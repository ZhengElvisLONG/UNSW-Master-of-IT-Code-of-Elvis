import re, math
from fractions import Fraction

shape_templates = {
    "Large triangle": {
        0: [("0", "0"), ("2", "2"), ("2", "0")],
        45: [("0", "0"), ("0", "2*sqrt(2)"), ("sqrt(2)", "sqrt(2)")],
    },
    "Small triangle": {
        0: [("0", "0"), ("1", "1"), ("1", "0")],
        45: [("0", "0"), ("0", "sqrt(2)"), ("0.5*sqrt(2)", "0.5*sqrt(2)")],
    },
    "Medium triangle": {
        0: [("0", "0"), ("1", "1"), ("2", "0")],
        45: [("0", "0"), ("0", "sqrt(2)"), ("sqrt(2)", "sqrt(2)")],
    },
    "Square": {
        0: [("0", "0"), ("0", "1"), ("1", "1"), ("1", "0")],
        45: [("0", "0"), ("-0.5*sqrt(2)", "0.5*sqrt(2)"), ("0", "sqrt(2)"), ("0.5*sqrt(2)", "0.5*sqrt(2)")],
    },
    "Parallelogram": {
        0: [("0", "0"), ("1", "1"), ("2", "1"), ("1", "0")],
        45: [("0", "0"), ("0.5*sqrt(2)", "0.5*sqrt(2)"), ("1.5*sqrt(2)", "0.5*sqrt(2)"), ("sqrt(2)", "0")],
    }
}

class Point:
    def __init__(self, x_expr, y_expr):
        self.x_rational, self.x_sqrt2 = self._parse_expr(x_expr)
        self.y_rational, self.y_sqrt2 = self._parse_expr(y_expr)

    def _parse_expr(self, expr_str):
        tokens = expr_str.replace(" ", "").replace("-", " -").replace("+", " +").split()
        rat_part = sqrt_part = Fraction(0)

        for tok in tokens:
            if "sqrt(2)" not in tok:
                rat_part += Fraction(tok)
            else:
                coef = tok.replace("sqrt(2)", "").replace("*", "")
                if coef in ("", "+"): sqrt_part += 1
                elif coef == "-": sqrt_part -= 1
                else: sqrt_part += Fraction(coef)
        return rat_part, sqrt_part
    
    def _format(self, rat_val, sqrt_val):
        if rat_val == 0 and sqrt_val == 0: return "0"
        segments = []
        if rat_val != 0: segments.append(str(rat_val))

        if sqrt_val != 0:
            is_neg = sqrt_val < 0
            if rat_val != 0: sqrt_val = abs(sqrt_val)
            
            if sqrt_val.denominator != 1: sqrt_text = f"({sqrt_val})√2"
            elif sqrt_val.numerator != 1 and sqrt_val.numerator != -1: sqrt_text = f"{sqrt_val}√2"
            elif sqrt_val.numerator == 1: sqrt_text = "√2"
            else: sqrt_text = "-√2"

            if rat_val == 0: segments.append(sqrt_text)
            else: segments.append(f"- {sqrt_text}" if is_neg else f"+ {sqrt_text}")
        return " ".join(segments)
    
    def _format_tex(self, rat_val, sqrt_val):
        if rat_val == 0 and sqrt_val == 0: return "0"
        tex_str = str(rat_val) if rat_val != 0 else ""

        if sqrt_val != 0:
            if sqrt_val > 0 and rat_val != 0: tex_str += "+"
            elif sqrt_val < 0: tex_str += "-"
            
            abs_coef = abs(sqrt_val)
            tex_str += "sqrt(2)" if abs_coef == 1 else f"{abs_coef} * sqrt(2)"

        return tex_str
    
    def __str__(self):
        return f"({self._format(self.x_rational, self.x_sqrt2)}, {self._format(self.y_rational, self.y_sqrt2)})"
    
    def rotate_90(self):
        self.x_rational, self.x_sqrt2, self.y_rational, self.y_sqrt2 = -self.y_rational, -self.y_sqrt2, self.x_rational, self.x_sqrt2

    def flip(self, x_flip=False, y_flip=False):
        if x_flip: self.x_rational, self.x_sqrt2 = -self.x_rational, -self.x_sqrt2
        if y_flip: self.y_rational, self.y_sqrt2 = -self.y_rational, -self.y_sqrt2

    def move(self, anchor_pt):
        self.x_rational += anchor_pt.x_rational; self.x_sqrt2 += anchor_pt.x_sqrt2
        self.y_rational += anchor_pt.y_rational; self.y_sqrt2 += anchor_pt.y_sqrt2

    def approx_x(self): return float(self.x_rational) + float(self.x_sqrt2) * 2 ** 0.5
    def approx_y(self): return float(self.y_rational) + float(self.y_sqrt2) * 2 ** 0.5
    
    def __eq__(self, other):
        return (self.x_rational == other.x_rational and self.x_sqrt2 == other.x_sqrt2 and 
                self.y_rational == other.y_rational and self.y_sqrt2 == other.y_sqrt2)

class Edge:
    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2
        self.vector = self._calculate_vector()

    def _calculate_vector(self):
        dx, dy = self.p2.approx_x() - self.p1.approx_x(), self.p2.approx_y() - self.p1.approx_y()
        vec_len = (dx**2 + dy**2)**0.5
        return (0.0, 0.0) if vec_len == 0 else (dx/vec_len, dy/vec_len)
    
    def get_direction_relation(self, other_edge):
        dx1, dy1 = self.vector
        dx2, dy2 = other_edge.vector
        dot_prod = dx1*dx2 + dy1*dy2
        
        if abs(dot_prod - 1.0) < 1e-8: dir_val = 1
        elif abs(dot_prod + 1.0) < 1e-8: dir_val = -1
        else: return 0
        
        test_edge = Edge(self.p1, other_edge.p1)
        tx, ty = test_edge.vector
        return 0 if abs(dx1*ty - dy1*tx) > 1e-8 else dir_val

class TangramPuzzle:
    def __init__(self, filename):
        with open(filename) as f: self.content = f.readlines()
        self.vertices = []
        self.transformations = self.parse_transfomations()
        self.vertices.sort(key=lambda s: (-s[1][0].approx_y(), s[1][0].approx_x(), s[1][1].approx_x()))

    def parse_transfomations(self):
        trans_dict = {}
        for line in self.content:
            if "PieceTangram" not in line: continue
            shape_name, x_flip, y_flip, rot = self.analyze_line(line)
            if shape_name in trans_dict: shape_name = shape_name.replace("1", "2")
            
            trans_info = {'rotate': rot, 'xflip': x_flip}
            if y_flip: trans_info['yflip'] = y_flip
            trans_dict[shape_name] = trans_info
        return trans_dict

    def analyze_line(self, line):
        type_to_name = {  
            "TangCar": "Square", "TangGrandTri": "Large triangle 1",
            "TangMoyTri": "Medium triangle", "TangPetTri": "Small triangle 1",
            "TangPara": "Parallelogram",
        }
        shape_type = re.findall(r"\{([^{}]*)\}", line)[-1]
        shape_name = type_to_name[shape_type]

        params = re.findall(r"<([^<>]*)>", line)
        if params: params = params[0].replace(" ", "").split(",")
        x_flip, y_flip, rot = self.cal_rotate(params)
        
        point_data = re.findall(r"\{([^{}]*)\}", line)[:2]
        self.compute_vertices(point_data, shape_name.replace(" 1", ""), x_flip, y_flip, rot)
        return shape_name, x_flip, y_flip, rot

    def cal_rotate(self, params):
        x_flip = y_flip = False
        rot = 0
        for p in params:
            name, val = p.split("=")
            if name == "xscale" and val == "-1": x_flip = True
            if name == "yscale" and val == "-1": y_flip = True
            if name == "rotate": rot = int(val)
        
        if x_flip and y_flip: rot += 180; x_flip = y_flip = False
        return x_flip, y_flip, rot % 360
    
    def compute_vertices(self, point_data, shape_name, x_flip, y_flip, rot):
        anchor = Point(point_data[0], point_data[1])
        base_angle = 0 if rot % 90 == 0 else 45
        base_coords = shape_templates[shape_name][base_angle]
        
        steps = (rot - base_angle) // 90
        points = [Point(x, y) for x, y in base_coords]
        for p in points:
            for _ in range(steps): p.rotate_90()
            p.flip(x_flip=x_flip, y_flip=y_flip)
            p.move(anchor)

        if x_flip != y_flip: points = points[::-1]

        top_left = min(points, key=lambda p: (-p.approx_y(), p.approx_x()))
        idx = points.index(top_left)
        points = points[idx:] + points[:idx]
        self.vertices.append((shape_name, points))
    
    def __str__(self):
        return "\n".join(f"{name:15}: [{', '.join(str(p) for p in pts)}]" for name, pts in self.vertices)

    def draw_pieces(self, filename):
        all_pts = [p for _, pts in self.vertices for p in pts]
        x_vals = [p.approx_x() for p in all_pts]
        y_vals = [p.approx_y() for p in all_pts]

        x_min, x_max = math.floor(min(x_vals)*2-1)/2, math.ceil(max(x_vals)*2+1)/2
        y_min, y_max = math.floor(min(y_vals)*2-1)/2, math.ceil(max(y_vals)*2+1)/2

        with open(filename, "w") as f:
            f.write("\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\n\\begin{tikzpicture}\n")
            f.write(f"\\draw[step=5mm] ({x_min}, {y_min}) grid ({x_max}, {y_max});\n")

            for _, pts in self.vertices:
                coords = [f"({{{p._format_tex(p.x_rational, p.x_sqrt2)}}}, {{{p._format_tex(p.y_rational, p.y_sqrt2)}}})" for p in pts]
                f.write(f"\\draw[ultra thick] {' -- '.join(coords)} -- cycle;\n")
            f.write(f"\\fill[red] (0,0) circle (3pt);\n\\end{tikzpicture}\n\n\\end{document}\n")

    def ger_all_edge(self):
        return [Edge(pts[i], pts[(i+1)%len(pts)]) for _, pts in self.vertices for i in range(len(pts))]
    
    def remove_opposite(self, edges):
        return [e1 for e1 in edges if not any(e1.p1 == e2.p2 and e1.p2 == e2.p1 for e2 in edges)]
    
    def merge_forward_edges(self, edges):
        changed = True
        while changed:
            changed = False
            new_edges, used = [], set()

            for e1 in edges:
                if e1 in used: continue
                merged = False
                for e2 in edges:
                    if e2 in used or e1 is e2: continue
                    if (e1.p2 == e2.p1 or e2.p2 == e1.p1) and e1.get_direction_relation(e2) == 1:
                        new_edge = Edge(e1.p1, e2.p2) if e1.p2 == e2.p1 else Edge(e2.p1, e1.p2)
                        new_edges.append(new_edge)
                        used.update([e1, e2])
                        changed = merged = True
                        break
                if not merged: new_edges.append(e1); used.add(e1)
            edges = new_edges
        return edges
    
    def merge_opposite_edges(self, edges):
        result, used = [], set()

        for e1 in edges:
            if e1 in used: continue
            merged = False

            for e2 in edges:
                if e2 in used or e1 is e2 or e1.get_direction_relation(e2) != -1: continue

                points = sorted([e1.p1, e1.p2, e2.p1, e2.p2], key=lambda p: (p.approx_x(), p.approx_y()))
                p0, p1, p2, p3 = points
    
                if ((p0 == e1.p1 and p1 == e1.p2) or (p0 == e1.p2 and p1 == e1.p1) or
                    (p0 == e2.p1 and p1 == e2.p2) or (p0 == e2.p2 and p1 == e2.p1)): continue
                    
                used.update([e1, e2])
                merged = True
    
                if e1.p1 != e2.p2: result.append(Edge(e1.p1, e2.p2))
                if e2.p1 != e1.p2: result.append(Edge(e2.p1, e1.p2))
                break

            if not merged: result.append(e1)
        return result
    
    def trace_closed_loop_backtrack(self, edges):
        start_pt = self.vertices[0][1][0]

        def backtrack(path, remaining, cur_pt):
            if not remaining: return path if cur_pt == start_pt else None
            
            for edge in [e for e in remaining if e.p1 == cur_pt]:
                next_rem = remaining.copy()
                next_rem.remove(edge)
                if result := backtrack(path + [edge], next_rem, edge.p2): return result
            return None
            
        return backtrack([], edges.copy(), start_pt)
    
    def draw_outline(self, filename):
        all_pts = [p for _, shape in self.vertices for p in shape]
        x_vals = [p.approx_x() for p in all_pts]
        y_vals = [p.approx_y() for p in all_pts]

        x_min, x_max = math.floor(min(x_vals)*2-1)/2, math.ceil(max(x_vals)*2+1)/2
        y_min, y_max = math.floor(min(y_vals)*2-1)/2, math.ceil(max(y_vals)*2+1)/2

        edges = self.ger_all_edge()
        edges = self.remove_opposite(edges)
        edges = self.merge_forward_edges(edges)
        edges = self.merge_opposite_edges(edges)
        final_edges = self.trace_closed_loop_backtrack(edges)

        with open(filename, "w") as f:
            f.write("\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\n\\begin{tikzpicture}\n")
            f.write(f"\\draw[step=5mm] ({x_min}, {y_min}) grid ({x_max}, {y_max});\n")
            
            if final_edges:
                coords = [f"({{{p._format_tex(p.x_rational, p.x_sqrt2)}}}, {{{p._format_tex(p.y_rational, p.y_sqrt2)}}})" for edge in final_edges for p in [edge.p1]]
                coords_str = ' --\n    '.join(coords)
                f.write(f"\\draw[ultra thick]\n    {coords_str} -- cycle;\n")
            
            f.write(f"\\fill[red] (0,0) circle (3pt);\n\\end{tikzpicture}\n\n\\end{document}\n")
