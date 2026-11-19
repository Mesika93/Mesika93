# Персонаж каналу — «Нуль» (фінальна версія)

## Чому не беремо персонажа з картинки 1:1
Надісланий лист персонажа — це практично маскот Day One Films: їхня аватарка (поза з
замкненими руками + золотий німб), біло-бежева голова, чорне худі. Якщо взяти його без змін:
- глядачі напишуть «копія Day One Films» → недовіра, дизлайки;
- ризик скарги від них на підробку бренду (impersonation) → страйк або видалення каналу;
- алгоритм показує їхнім глядачам їх, а не тебе — тобі потрібна власна впізнаваність.

**Беремо від них стиль (жирний контур, прості емоції, темний фон), але змінюємо 4 речі:**

| | Day One Films | Наш «Нуль» |
|---|---|---|
| Шкіра | біло-бежева | **холодна сіро-блакитна** |
| Одяг | чорне худі | **паленo-помаранчеве худі (burnt orange)**, сірі шнурки |
| Фірмова деталь | — | **маленький пластир на лівій щоці** (символ: «падав, але встав») |
| Аватарка | золотий німб, руки замкнені | **помаранчеве сонце, що сходить**, позаду; персонаж застібає худі, погляд рішучий |

---

## Майстер-промпт (вставляти на початок КОЖНОГО кадру)
```
2D cartoon character "Zero": simple round bald head, smooth cool grey-blue skin,
small solid black dot eyes, thick black expressive eyebrows, small simple mouth, no nose, no ears,
small beige bandage on his left cheek, oversized burnt-orange hoodie with grey drawstrings,
dark grey pants, simple white hands with 4 fingers, bold black outline,
flat cel shading, sticker-like clean style
```

## Лист персонажа (згенерувати першим)
```
[MASTER PROMPT], character reference sheet, front view, 3/4 view, side view, back view,
full body, neutral pose, plain dark charcoal background, consistent proportions, no text
```

## Лист емоцій (другим)
```
[MASTER PROMPT], emotion sheet, 4x3 grid of bust portraits on dark background:
determined, angry with red glowing eyes, sad crying with blue tears, shocked with white wide eyes,
tired with heavy eyelids, laughing, confused with question mark, embarrassed blushing,
sleeping with zzz, thinking hand on chin, cool with black sunglasses, holding a coffee mug,
consistent character in every cell, no text
```

## Аватарка каналу
```
[MASTER PROMPT], bust portrait, zipping up his orange hoodie, determined focused eyes,
large glowing orange rising sun circle behind him, dark night-to-dawn gradient background,
small golden sparkles, centered composition, 1:1
```

## Батьки (для відео №1)
```
same art style as Zero: 2D cartoon elderly mother, round grey-blue head, small dot eyes,
grey hair in a bun, soft beige cardigan, kind tired smile; elderly father, bald round grey-blue head,
grey side hair, small round glasses, brown knitted sweater, slightly hunched;
bold black outline, flat cel shading, front and side views, dark background, no text
```

---

## Правила, щоб персонаж був однаковим у всіх кадрах
1. Згенеруй лист персонажа → вибери **одну** найкращу картинку = «еталон».
2. Midjourney: до кожного кадру додавай `--cref <URL еталону> --cw 100 --ar 16:9`.
   ChatGPT: прикріплюй еталон і пиши *"Use this exact character, same face, same hoodie, same bandage."*
3. Кольори завжди називати однаково: **grey-blue skin**, **burnt-orange hoodie**.
4. Якщо пластир чи колір зник — перегенеруй, не залишай (саме це робить персонажа «твоїм»).
5. Лист емоцій із кроку вище використовуй також для прев'ю та Shorts-стікерів (BRO… / GG / LOL — як у твоїй картинці, це гарна ідея, лишаємо).

## Відповідність емоцій кадрам відео №1
| Кадр | Емоція |
|---|---|
| 1–2 | байдужий / втомлений |
| 5 | злий підліток |
| 10 | плаче (сльози) |
| 11 | рішучий |
| 13–14 | тепла усмішка |
