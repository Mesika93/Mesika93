# Відео №1 — «Your Parents Are Getting Older.»

**Рішення за замовчуванням** (можна змінити будь-коли):
- Мова: **англійська озвучка + українські субтитри** (і окрема українська версія для Shorts).
- Персонаж: **«Нуль»**. Сіро-синій лисий чоловічок, помаранчеве худі.
- Інструменти: **ChatGPT (images) або Midjourney** → **Kling / Hailuo** (анімація) → **ElevenLabs** (голос) → **CapCut** (монтаж).
- Формат: 16:9, 1920×1080, ~2:40.

---

## КРОК 1. Створи персонажа (робиться 1 раз для всього каналу)

> ✅ **Фінальні промпти персонажа — у [`../CHARACTER.md`](../CHARACTER.md)** (сіро-блакитна шкіра, помаранчеве худі, пластир на щоці).
> У кожен промпт кадру нижче додавай на початок **MASTER PROMPT** звідти. Промпти 1.1–1.3 нижче — старіша чернетка.

### 1.1 Головний референс
```
2D animated character design sheet, simple cartoon man, completely bald round head,
smooth grey-blue skin, small black dot eyes, thick expressive dark eyebrows, small mouth,
no nose, slightly chubby simple body, wearing an oversized burnt-orange hoodie and dark grey pants,
front view, side view, back view, plain dark charcoal background,
clean bold outlines, soft cel shading, cinematic warm rim light, consistent proportions
```

### 1.2 Лист емоцій
```
same character, expression sheet, 6 faces in a grid: sad with teary eyes, angry, tired with dark circles,
shocked, determined, smiling warmly, grey-blue bald cartoon man, orange hoodie, dark background, 2D cel shading
```

### 1.3 Батьки (теж 1 раз)
```
2D cartoon character design, same art style as reference: simple round-headed elderly mother,
grey-blue skin, small dot eyes, grey hair in a bun, soft beige cardigan, kind tired smile;
and elderly father, bald with grey side hair, small round glasses, brown sweater, slightly hunched,
front and side views, dark background, clean outlines, soft cel shading
```

**Важливо:** збережи найкращі картинки. Потім у **кожен** промпт додавай референс:
- Midjourney: `--cref <URL персонажа> --cw 100 --ar 16:9`
- ChatGPT: завантаж картинку персонажа й напиши «use this exact character».

Стиль, який додається в кінець КОЖНОГО кадру (далі позначено як `[STYLE]`):
```
2D animated short film still, clean bold outlines, soft cel shading, cinematic lighting,
moody dark palette with warm orange accent light, shallow depth of field, 16:9
```

---

## КРОК 2. Кадри: картинка → анімація

| # | Тривалість | Промпт для картинки (+ `[STYLE]`) | Промпт для анімації (Kling/Hailuo, 5 с) |
|---|---|---|---|
| 1 | 6 с | Close-up of a smartphone vibrating on a dark wooden desk, screen shows incoming call "Mom ❤", the character's hand reaching to press the red decline button, cold blue screen glow | phone vibrates, hand slowly presses decline, screen goes dark, slow push-in |
| 2 | 6 с | The character in orange hoodie sitting in a dark room wearing big headphones, playing video games, face lit by monitor, empty energy drink cans | character's eyes move following the game, subtle breathing, flicker of monitor light |
| 3 | 10 с | Warm golden flashback: young father carrying the character as a small child on his shoulders in a sunny park, both laughing, soft film grain | child laughs and raises arms, dad walks forward, warm light flickers through trees |
| 4 | 10 с | Sunny suburban street, young mother running behind a small child on a red bicycle, holding the seat, child smiling, warm nostalgic light | mother runs and lets go of the seat, child rides away, camera tracks sideways |
| 5 | 13 с | Teenage version of the character slamming a bedroom door, parents sitting silently at a dinner table in the background, cold grey light | door slams shut, parents' heads lower slowly, light dims |
| 6 | 15 с | Elderly mother alone in a small cozy kitchen at evening, table set with two plates, one plate empty, steam from food, warm lamp light, rain on window | mother looks at the empty chair, sighs softly, steam rises, rain on window |
| 7 | 12 с | Elderly father slowly climbing narrow stairs holding the handrail, his hand trembling, dim hallway light | father takes one slow step, pauses to breathe, hand trembles on rail |
| 8 | 13 с | Large hourglass on a dark surface, inside the falling sand there is a small family photo, warm orange backlight | sand falls steadily, photo slowly gets buried, slow zoom in |
| 9 | 15 с | **Текстовий кадр у CapCut, без генерації:** чорний фон, білий текст «5 visits a year × 20 years = **100**» | Текст з'являється по рядку, «100» збільшується з легким тремтінням |
| 10 | 12 с | Close-up of the character in dark room staring at phone screen showing "Mom — 7 missed calls", tears forming, face lit by phone | tear slowly rolls down cheek, slight trembling, very slow push-in |
| 11 | 8 с | Character's thumb pressing the green call button, phone screen "Calling Mom…" | thumb presses call button, screen animates calling |
| 12 | 8 с | Elderly mother in the kitchen picking up an old phone, her face lighting up with surprise and joy, warm light | mother's face turns from tired to joyful, she holds phone with both hands |
| 13a | 7 с | Character sitting by a bus window at sunrise, holding a bag, calm hopeful face | landscape passes outside window, sunlight moves across his face |
| 13b | 7 с | Doorway of an old apartment, mother hugging the character tightly, father smiling behind her | mother hugs him, father puts hand on his shoulder |
| 13c | 8 с | The family of three at the kitchen table laughing, warm lamp, food on all plates | everyone laughs, father gestures while telling a story |
| 14 | 8 с | Three silhouettes sitting on a bench on a hill at sunset, the character in the middle, orange sky | sun sets slowly, hair and clothes move in wind, slow pull-out |
| 15 | 5 с | **Текстовий кадр у CapCut:** чорний екран, «Call them today.» | fade in, тримати 3 с, fade out |

Порада: генеруй по **3–4 варіанти** кожного кадру і бери той, де персонаж найбільше схожий на референс. Якщо анімація «пливе», просто зроби повільний zoom у CapCut.

---

## КРОК 3. Озвучка (ElevenLabs)

**Налаштування:** глибокий спокійний чоловічий голос (наприклад *Brian*, *Adam* чи *Callum*), Stability 40%, Similarity 75%, Style 15%.
`<break time="1.0s" />` — це паузи, вставляй як є.

```
You declined her call again. <break time="1.0s" />
"I'll call her back later." <break time="1.5s" />

Remember when they were your whole world? <break time="1.0s" />
She ran behind you… so you wouldn't fall. <break time="1.5s" />

Then you grew up. <break time="0.7s" /> And they became… annoying. <break time="2.0s" />

She still cooks for two. <break time="0.7s" /> Just in case you visit. <break time="1.5s" />
His hands shake now. <break time="0.5s" /> He won't tell you. <break time="2.0s" />

You think you have time. <break time="0.8s" />
You see them maybe five times a year. <break time="1.0s" />
If they live twenty more years… <break time="1.0s" />
that's one hundred visits. <break time="0.8s" /> Left. <break time="2.5s" />

One day… the phone will stop ringing. <break time="2.0s" />

So call her. <break time="3.0s" />

Not because you have to. <break time="0.8s" />
Because one day… you won't be able to. <break time="1.5s" />

They gave you their whole life. <break time="0.8s" />
Give them an hour. <break time="2.0s" />

Call them today.
```

Голос мами для кадру 12 (окремо, жіночий літній голос, тихо):
```
Hello? <break time="0.5s" /> Sweetheart? <break time="0.5s" /> Is everything okay?
```

---

## КРОК 4. Музика і звуки

| Відрізок | Що ставити | Де взяти |
|---|---|---|
| 0:00–0:12 | Тиша + вібрація телефону + гул кімнати | YouTube Audio Library (SFX) |
| 0:12–1:40 | Сумне повільне піаніно | YouTube Audio Library: пошук «sad piano», «emotional» |
| 1:40–1:52 | **Повна тиша** (тільки голос) — найсильніший момент | — |
| 1:52–2:00 | Гудки дзвінка | SFX |
| 2:00–2:40 | Теплий наростаючий трек (струнні + піаніно) | пошук «inspiring cinematic», «hopeful» |

Гучність: музика −22…−18 dB під голосом, голос −6 dB.

---

## КРОК 5. Монтаж (CapCut)

1. Закинь озвучку на таймлайн першою, потім підганяй кадри під фрази.
2. Кожен кадр: повільний zoom 100% → 108% (якщо немає анімації).
3. Переходи: звичайні склейки; у флешбеках (кадри 3–4) — плавні переходи + тепла кольорокорекція + плівкове зерно.
4. Субтитри: білий жирний шрифт (Montserrat ExtraBold), по центру знизу, **2–4 слова** за раз. Українські — з файлу `subtitles_uk.srt`.
5. Кадр 9 (цифра «100») — звук удару серця в момент появи.
6. Експорт: 1080p, 30 fps.

---

## КРОК 6. Прев'ю (3 варіанти для A/B тесту)

**A — LAST CALL.**
```
YouTube thumbnail, the grey-blue bald cartoon character in orange hoodie holding a phone,
screen shows "Mom - 7 missed calls", teary guilty eyes, dark background, warm orange rim light,
high contrast, expressive face, empty space at top for text
```
Текст зверху: **LAST CALL.** (білий, дуже жирний, з чорною обводкою)

**B — 100.**
Елементи: мама дивиться у вікно, на склі велике **100.** → питання «100 чого?» змушує клікнути.

**C — TOO LATE.**
Елементи: порожній стілець за кухонним столом, друга тарілка, тепле світло, напис **TOO LATE.**

---

## КРОК 7. Публікація

**Назва (варіанти):**
1. Your Parents Are Getting Older.
2. You Only Have 100 Visits Left With Your Parents
3. Call Your Mom. | An Animated Short Film

**Опис:**
```
They gave you their whole life. Give them an hour.

An animated short film about time, family, and the calls we keep declining.

If this made you think of someone — call them today.

#shortfilm #animation #motivation #parents #family
```

**Теги:** animated short film, parents getting older, call your mom, motivation, emotional animation, self improvement, family, life lessons

**Shorts з цього відео:**
1. Кадри 6–9 («She still cooks for two… 100 visits. Left.»), 30 с.
2. Кадри 10–12 (дзвінок і реакція мами), 25 с.
3. Українська версія кадрів 6–9 з українським голосом.

---

## Чекліст
- [ ] Персонаж + батьки (крок 1)
- [ ] 17 картинок кадрів
- [ ] Анімація кадрів
- [ ] Озвучка EN + голос мами
- [ ] Музика + SFX
- [ ] Монтаж + субтитри
- [ ] 3 прев'ю
- [ ] Публікація + 3 Shorts
