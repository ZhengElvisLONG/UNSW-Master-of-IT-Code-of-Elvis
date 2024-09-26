from graphviz import Graph

def create_detailed_er_diagram():
    dot = Graph(comment='Detailed Hospital ER Diagram', engine='neato')
    dot.attr(rankdir='TB', size='200,200', overlap='false')


    # Entities
    entities = ['Doctors', 'Departments', 'Patients', 'Medications', 'Prescriptions', 'Rooms', 'Equipment']
    for entity in entities:
        dot.node(entity, entity, shape='box', style='filled', fillcolor='lightblue')

    # Attributes with underline for important ones
    attributes = {
        'Doctors': [('staff_id', True), ('name', False), ('specialty', False), ('years_of_experience', False)],
        'Departments': [('department_id', True), ('department_name', False), ('description', False), ('location', False)],
        'Patients': [('SSN', True), ('name', False), ('address', False), ('age', False), ('date_of_birth', False), ('phone_number', False)],
        'Medications': [('medication_id', True), ('medication_name', False), ('description', False), ('price', False)],
        'Prescriptions': [('prescription_id', True), ('date', False)],
        'Rooms': [('room_id', True), ('location', False), ('room_type', False)],
        'Equipment': [('equipment_id', True), ('equipment_name', False), ('type', False), ('description', False)]
    }

    for entity, attrs in attributes.items():
        for attr, is_important in attrs:
            attr_name = f"{entity}_{attr}"
            label = f"<u>{attr}</u>" if is_important else attr
            dot.node(attr_name, f'<<font face="Arial">{label}</font>>', shape='ellipse')
            dot.edge(entity, attr_name, style='solid')

    # Special handling for patient's name
    dot.node('Patients_first_name', 'first_name', shape='ellipse')
    dot.node('Patients_last_name', 'last_name', shape='ellipse')
    dot.edge('Patients_name', 'Patients_first_name', style='solid')
    dot.edge('Patients_name', 'Patients_last_name', style='solid')

    # Relationships with double lines for 'n' cardinality
    relationships = [
        ('Doctors', 'Departments', 'works_in', '1', 'n'),
        ('Patients', 'Prescriptions', 'receives', '1', 'n'),
        ('Doctors', 'Prescriptions', 'prescribes', '1', 'n'),
        ('Prescriptions', 'Medications', 'includes', 'm', 'n'),
        ('Departments', 'Rooms', 'has', '1', 'n'),
        ('Patients', 'Rooms', 'assigned_to', 'm', 'n'),
        ('Departments', 'Equipment', 'owns', '1', 'n')
    ]

    for start, end, label, start_card, end_card in relationships:
        rel_name = f"{start}_{end}_{label}"
        dot.node(rel_name, label, shape='diamond', style='filled', fillcolor='lightyellow')
        
        # Use double lines for 'n' or 'm' cardinality
        start_style = 'setlinewidth(2)' if start_card in ['n', 'm'] else ''
        end_style = 'setlinewidth(2)' if end_card in ['n', 'm'] else ''
        
        dot.edge(start, rel_name, label=start_card, style=start_style)
        dot.edge(rel_name, end, label=end_card, style=end_style)

    # Special handling for 'assigned_to' relationship
    dot.node('assigned_to_details1', 'start_time', shape='ellipse')
    dot.edge('Patients_Rooms_assigned_to', 'assigned_to_details1', style='solid')
    dot.node('assigned_to_details2', 'end_time', shape='ellipse')
    dot.edge('Patients_Rooms_assigned_to', 'assigned_to_details2', style='solid')
    dot.node('assigned_to_details3', 'available_rooms', shape='ellipse')
    dot.edge('Patients_Rooms_assigned_to', 'assigned_to_details3', style='solid')

    return dot

# Generate and save the diagram
er_diagram = create_detailed_er_diagram()
er_diagram.render('hospital_er_diagram_detailed', format='png', cleanup=True)
print("Detailed ER diagram has been generated as 'hospital_er_diagram_detailed.png'")