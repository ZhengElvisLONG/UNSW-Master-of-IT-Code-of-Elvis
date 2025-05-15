# Purpose Statement
<!-- **English**   -->
The UNSW Developmental Wind Farm project aims to support UNSW's 2025 strategic goals by developing a sustainable energy solution that integrates teaching, research, and operations. The project will provide a platform for renewable energy research while reducing the university's carbon footprint.

<!-- **中文**
UNSW 开发风电场项目旨在通过开发一种可持续的能源解决方案来支持 UNSW 的 2025 战略目标，该解决方案将教学、研究和运营整合在一起。该项目将为可再生能源研究提供平台，同时减少大学的碳足迹。 -->
---

# Scope Statement
<!-- **English**   -->
The project scope covers the full lifecycle of developing UNSW's 30MW scalable wind farm, including strategic alignment, engineering design with future expansion capacity, regulatory-compliant construction, and operational integration with research systems. Core components:  
- Scalable infrastructure for 8→10 turbine units  
- Remote monitoring system integrated with campus  
- Full compliance with NSW planning and heritage regulations  
- Maintenance systems supporting 10-year operations  

<!-- **中文**  
项目范围涵盖UNSW可扩展风电场的全生命周期开发，包含战略对齐、预留扩展的工程设计、合规施工及与研究系统的运营整合。核心要素：  
- 8→10台风机的可扩展基础设施  
- 与校园集成的远程监控系统  
- 符合新州规划及文化遗产法规  
- 支持10年运维的维护体系 -->

---

# Key Deliverables
<!-- **English**   -->
1. Strategic Alignment Report (UNSW 2025 Gap Analysis)  
2. Scalable Turbine Layout Blueprint (10-unit capacity)  
3. NSW Planning Portal Submission Package  
4. As-built Drawings with Heritage Protection Notes  
5. SCADA Integration Test Certificates  
6. Annual Performance Report Template  
7. Blade Recycling Protocol  
8. Digital Twin Model (BIM Level 3)  

<!-- **中文**  
1. 战略对齐报告（UNSW 2025差距分析）  
2. 可扩展风机布局蓝图（10台容量）  
3. 新州规划门户申报包  
4. 含遗产保护注释的竣工图纸  
5. SCADA系统集成测试证书  
6. 年度性能报告模板  
7. 叶片回收协议  
8. 数字孪生模型（BIM三级）   -->

---

# Constraints
<!-- **English**   -->
- **Budget**: Fixed at AUD $48M (designated for 8 turbines)  
- **Duration**: Shortest feasible timeline (commissioning ≤24 months)  
- **Regulatory**: Mandatory Aboriginal heritage surveys prior to earthworks  
- **Technical**: Minimum 30MW electrical system capacity for future expansion  
- **Social**: Ongoing wildlife impact monitoring during operations  

<!-- **中文**  
- **预算**: 固定4800万澳元（8台风机专项）  
- **工期**: 最短可行时间（调试≤24个月）  
- **法规**: 土方工程前强制土著遗产调查  
- **技术**: 未来扩展需30MW电气系统容量  
- **社会**: 运营期间持续野生动物影响监测 -->
---
# Code for WBS Graph
```mermaid
graph TD
    %% 主项目结构
    A[UNSW Developmental Wind Farm WBS] --> B[1 Project Initiation] %% 1. 项目启动
    A --> C[2 Engineering Design] %% 2. 工程设计
    A --> D[3 Procurement & Bidding] %% 3. 招标采购
    A --> E[4 Construction] %% 4. 施工
    A --> F[5 Commissioning & Testing] %% 5. 调试测试
    A --> G[6 Project Management] %% 6. 项目管理
    A --> H[7 Compliance & Documentation] %% 7. 合规文档
    A --> I[8 Operations & Maintenance] %% 8. 运维

    %% 项目启动
    B[1 Project Initiation] --> B1[1.1 Strategic Alignment] %% 1.1 战略对齐
    B --> B2[1.2 Feasibility Study] %% 1.2 可行性研究

    %% 工程设计
    C[2 Engineering Design] --> C1[2.1 Conceptual Design] %% 2.1 概念设计
    C --> C2[2.2 Design Drawings and Document (Detialed Design)] %% 2.2 详细设计

    %% 招标采购
    D[3 Procurement & Bidding] --> D1[3.1 Tender Process] %% 3.1 招标流程
    D --> D2[3.2 Contract Execution] %% 3.2 合同执行

    %% 施工
    E[4 Construction] --> E1[4.1 Site Works] %% 4.1 场地工程
    E --> E2[4.2 Foundation] %% 4.2 基础
    E --> E3[4.3 Electrical] %% 4.3 电气工程

    %% 调试测试
    F[5 Commissioning & Testing] --> F1[5.1 Unit Testing] %% 5.1 单元测试
    F --> F2[5.2 System Testing] %% 5.2 系统测试
    F --> F3[5.3 Remote Systems] %% 5.3 远程系统

    %% 项目管理
    G[6 Project Management] --> G1[6.1 Cost Control] %% 6.1 成本控制
    G --> G2[6.2 Risk Mgmt] %% 6.2 风险管理
    G --> G3[6.3 Digital Tools] %% 6.3 数字工具

    %% 合规文档
    H[7 Compliance & Documentation] --> H1[7.1 Compliance Process (Approvals)] %% 7.1 合规审批
    H --> H2[7.2 Deliverables] %% 7.2 交付物

    %% 运维
    I[8 Operations & Maintenance] --> I1[8.1 Performance] %% 8.1 性能
    I --> I2[8.2 Sustainability] %% 8.2 可持续性

    %% 关键路径
    C1[2.1 Conceptual Design] -.->|Layout Finalized| D1[3.1 Tender Process] %% 布局确定
    D2[3.2 Contract Execution] -.->|Contract Signed| E1[4.1 Site Works] %% 合同签署
    E3[4.3 Electrical] -.->|Power Ready| F2[5.2 System Testing] %% 电力就绪
    F2[5.2 System Testing] -.->|Grid Approved| I1[8.1 Performance] %% 电网批准
    H1[7.1 Approvals] -.->|Permit Released| E1[4.1 Site Works] %% 许可发布

    %% 样式定义
    classDef phase fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef critical fill:#ffebee,stroke:#c62828
    class B,C,D,E,F,G,H,I phase
    class H1,B1 critical
```
---