# Shared Revenue Module

Descripton:
This module is responsible for handling shared revenue between organizations.

## ERD of models

```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        -id: Integer
        -created_at: DateTime
        -updated_at: DateTime
    }
    class PartnershipLevel {
        -name: CharField
        -description: CharField
        -percentage: DecimalField
        +revenue_partnership_levels: RevenueConfiguration[]
        +__str__(): str
    }
    class RevenueConfiguration {
        -organization: ForeignKey
        -course_code: CharField
        -partnership_level: ForeignKey
        -start_date: DateTimeField
        -end_date: DateTimeField
        +__str__(): str
    }
    class ShareExecution {
        -organization: ForeignKey
        -revenue_configuration: JSONField
        -percentage: DecimalField
        -value: DecimalField
        -receipt: CharField
        -executed: BooleanField
        -response_payload: JSONField
        +__str__(): str
    }
    PartnershipLevel |-- RevenueConfiguration
    BaseModel |-- PartnershipLevel
    BaseModel |-- RevenueConfiguration
    BaseModel |-- ShareExecution
    ShareExecution "1" -- "1" Organization : organization
    RevenueConfiguration "1" -- "1" PartnershipLevel : partnership_level
```
