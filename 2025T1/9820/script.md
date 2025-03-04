# Scope Statement | 范围说明
**English**  
The project scope covers the full lifecycle of developing UNSW's 30MW scalable wind farm, including strategic alignment, engineering design with future expansion capacity, regulatory-compliant construction, and operational integration with research systems. Core components:  
- Scalable infrastructure for 8→10 turbine units  
- Remote monitoring system integrated with campus  
- Full compliance with NSW planning and heritage regulations  
- Maintenance systems supporting 10-year operations  

**中文**  
项目范围涵盖UNSW可扩展风电场的全生命周期开发，包含战略对齐、预留扩展的工程设计、合规施工及与研究系统的运营整合。核心要素：  
- 8→10台风机的可扩展基础设施  
- 与校园集成的远程监控系统  
- 符合新州规划及文化遗产法规  
- 支持10年运维的维护体系

---

# Key Deliverables | 关键交付成果
**English**  
1. Strategic Alignment Report (UNSW 2025 Gap Analysis)  
2. Scalable Turbine Layout Blueprint (10-unit capacity)  
3. NSW Planning Portal Submission Package  
4. As-built Drawings with Heritage Protection Notes  
5. SCADA Integration Test Certificates  
6. Annual Performance Report Template  
7. Blade Recycling Protocol  
8. Digital Twin Model (BIM Level 3)  

**中文**  
1. 战略对齐报告（UNSW 2025差距分析）  
2. 可扩展风机布局蓝图（10台容量）  
3. 新州规划门户申报包  
4. 含遗产保护注释的竣工图纸  
5. SCADA系统集成测试证书  
6. 年度性能报告模板  
7. 叶片回收协议  
8. 数字孪生模型（BIM三级）  

---

# Constraints | 约束条件
**English**  
- **Budget**: Fixed at AUD $48M (designated for 8 turbines)  
- **Duration**: Shortest feasible timeline (commissioning ≤24 months)  
- **Regulatory**: Mandatory Aboriginal heritage surveys prior to earthworks  
- **Technical**: Minimum 30MW electrical system capacity for future expansion  
- **Social**: Ongoing wildlife impact monitoring during operations  

**中文**  
- **预算**: 固定4800万澳元（8台风机专项）  
- **工期**: 最短可行时间（调试≤24个月）  
- **法规**: 土方工程前强制土著遗产调查  
- **技术**: 未来扩展需30MW电气系统容量  
- **社会**: 运营期间持续野生动物影响监测
---
# WBS Graph | 工作拆分图
```mermaid
graph TD
    %% 主项目结构
    A[UNSW Developmental Wind Farm WBS] --> B[Project Initiation]
    A --> C[Engineering Design]
    A --> D[Procurement & Bidding]
    A --> E[Construction]
    A --> F[Commissioning & Testing]
    A --> G[Project Management]
    A --> H[Compliance & Documentation]
    A --> I[Operations & Maintenance]

    %% 项目启动
    subgraph B[Project Initiation]
        B1[Strategic Alignment] --> B1a[UNSW 2025 Gap Analysis]
        B1 --> B1b[Teaching-Research Plan]
        B2[Feasibility Study] --> B2a[Wind Resource Assessment]
        B2 --> B2b[Grid Connection Study]
        B2 --> B2c[Budget Estimation]
    end

    %% 工程设计
    subgraph C[Engineering Design]
        C1[Conceptual Design] --> C1a[Site Topography]
        C1 --> C1b[Turbine Layout Optimization]
        C1 --> C1c[Modular Switchyard]
        
        C2[Detailed Design] --> C2a[Geotechnical Surveys]
        C2 --> C2b[Foundation Design]
        C2 --> C2c[SCADA Architecture]
        C2 --> C2d[Experimental Interfaces]
    end

    %% 招标采购
    subgraph D[Procurement & Bidding]
        D1[Tender Process] --> D1a[Bidding Documents]
        D1 --> D1b[Supplier Qualification]
        D2[Contract Execution] --> D2a[Risk Allocation]
        D2 --> D2b[Contract Clauses]
    end

    %% 施工
    subgraph E[Construction]
        E1[Site Works] --> E1a[Land Preparation]
        E1 --> E1b[Heritage Protection]
        E2[Foundation] --> E2a[Anchor Installation]
        E2 --> E2b[Concrete Works]
        E3[Electrical] --> E3a[Cable Installation]
        E3 --> E3b[Switchyard Build]
    end

    %% 调试测试
    subgraph F[Commissioning & Testing]
        F1[Unit Testing] --> F1a[Turbine Certification]
        F2[System Testing] --> F2a[Grid Integration]
        F3[Remote Systems] --> F3a[SCADA Setup]
        F3 --> F3b[Data Validation]
    end

    %% 项目管理
    subgraph G[Project Management]
        G1[Cost Control] --> G1a[Budget Tracking]
        G1 --> G1b[Change Control]
        G2[Risk Mgmt] --> G2a[Risk Modeling]
        G2 --> G2b[Weather Planning]
        G3[Digital Tools] --> G3a[4D Modeling]
    end

    %% 合规文档
    subgraph H[Compliance & Documentation]
        H1[Approvals] --> H1a[Development Permits]
        H1 --> H1b[Environmental Compliance]
        H2[Deliverables] --> H2a[Construction Drawings]
        H2 --> H2b[Test Reports]
        H2 --> H2c[Operation Manuals]
    end

    %% 运维
    subgraph I[Operations & Maintenance]
        I1[Performance] --> I1a[Annual Reporting]
        I1 --> I1b[Research Integration]
        I2[Sustainability] --> I2a[Recycling Program]
        I2 --> I2b[Wildlife Monitoring]
    end

    %% 关键路径
    C1b -->|Layout Finalized| D1a
    D2a -->|Contract Signed| E1a
    E3b -->|Power Ready| F2a
    F2a -->|Grid Approved| I1a
    H1a -->|Permit Released| E1b

    %% 样式定义
    classDef phase fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef critical fill:#ffebee,stroke:#c62828
    class B,C,D,E,F,G,H,I phase
    class H1a,B1a critical
```
---