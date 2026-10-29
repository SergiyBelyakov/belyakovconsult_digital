# Останній запуск конвеєра

Режим: dry-run. Оброблено дописів: 2. Час: 2026-10-29 16:16
Повідомлення в Telegram-адмінку: ні (секрети не задані)

## 1

```
🧪 Тестовий режим. Зараз вийшов би допис у Telegram (completeness-is-not-quality):

**98% заповненості не означає 98% якості**

Звіт каже: поле «номер документа» заповнене у 98% записів. Формально правда. Але повнота перевіряє лише, чи є в полі хоч щось, і чесно зараховує туди «0», «-», дату замість номера та серію, записану в поле номера.

Чого повнота не бачить:
• формату
• допустимих значень
• заглушок на кшталт «невідомо» чи «01.01.1900»
• узгодженості між полями
• унікальності

**Завдання на 15 хвилин.** Візьміть ключове поле свого реєстру і порахуйте дві цифри: «заповнено» і «проходить бізнес-правило». Якщо їх показати керівництву поруч, розмова про якість даних зазвичай стає набагато предметнішою.

Приклади й перелік перевірок: https://www.belyakovconsult.com/insights/completeness-is-not-quality/?utm_source=telegram&utm_medium=social&utm_campaign=completeness-is-not-quality
```

## 2

```
🧪 Тестовий режим. Зараз вийшов би допис у LinkedIn (completeness-is-not-quality):

The “document number” field is 98% complete. The quality report glows green, and technically it is not lying.

The catch: completeness answers only one question. Is there anything in the field at all? And “anything” covers a lot. In an illustrative register, the same 98% happily includes:

• “0” and “-”, typed so the form would finally agree to save
• a date where the number should be
• a document series typed into the number field
• six values where the reference list allows two

Completeness is like checking that an envelope has a sheet of paper inside. It says nothing about what is written on it. (The analogy has limits: in data, the sheet is sometimes in someone else’s envelope, meaning the record belongs to the wrong person.) What we actually care about is fitness for use.

How to check your own data in half an hour:
1. Pick one field a decision depends on: a payment, a register match, coverage.
2. Write down, in plain words, the rule a valid value must follow.
3. Count two numbers: “filled in” and “passes the rule”.

If the second is noticeably smaller, you have just found the real size of your data quality work. And probably a place where the report says something other than what leadership thinks it says.

Examples and checks: https://www.belyakovconsult.com/en/insights/completeness-is-not-quality/?utm_source=linkedin&utm_medium=social&utm_campaign=completeness-is-not-quality

#DataQuality #DataGovernance #PublicSector
```
