# Звіт по лабораторній роботі 1

**Автор:** Чех Анна    

## Plan
- **Обрана гра:** Arkanoid  
- **Діаграми:**  
  - [Use Case Diagram](diagrams/use_case.jpg)  
  - [Activity Diagram](diagrams/activity.jpg)  
  - [Class Diagram](diagrams/class_diagram.jpg)  

## Code
- **Клас Paddle:** Рух платформи  
- **Клас Ball:** Рух м’яча та зіткнення  
- **Клас Brick:** Блоки, які знищуються при зіткненні  
- **Клас Game:** Логіка гри, "Play again" (Y/N), зміна фону  
- **Функції:** Підтримка аргументів (`--difficulty`, `--bg-color`)  

## Build
| Тест           | Результат  |
|----------------|------------|
| Рух платформи  | Успішно    |
| Зіткнення      | Успішно    |
| Знищення блоків| Успішно    |
| Перемога       | Успішно    |
| Програш        | Успішно    |
| Зміна кольору  | Успішно    |

## Інструкції
- **Запустити:**  
  - `python arkanoid.py --difficulty medium`  
  - `python arkanoid.py --bg-color pink` (або інший колір: red, blue)  
