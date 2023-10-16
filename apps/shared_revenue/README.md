# Shared Revenue Module

Descripton:
This module is responsible for handling shared revenue between organizations.

## ERD of models

```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        -id: IntegerField
        -created_at: DateTimeField
        -updated_at: DateTimeField
    }
    class Organization {
        <<external>>
    }
    class RevenueConfiguration {
        -organization: ForeignKey(Organization)
        -course_code: CharField
        -partner_percentage: DecimalField
        -start_date: DateTimeField
        -end_date: DateTimeField
        +__str__(): str
    }
    class Receipt {
        <<external>>
    }
    class ShareExecution {
        -organization: ForeignKey(Organization)
        -revenue_configuration: JSONField
        -percentage: DecimalField
        -value: DecimalField
        -receipt: CharField
        -executed: BooleanField
        -response_payload: JSONField
        +__str__(): str
    }
    BaseModel <|-- RevenueConfiguration
    BaseModel <|-- ShareExecution
    Organization <.. RevenueConfiguration
    Receipt <.. ShareExecution
```
