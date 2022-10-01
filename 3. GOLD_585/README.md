# # Задание:

Компания выдает купоны на подарки с целью привлечения новых клиентов через акции с партнерами «585*ЗОЛОТОЙ». Бюджет на подарки – 3 млн. руб. в месяц (по себестоимости подарков). Если происходит перерасход, то требуется дополнительное согласование с руководством. Остаток подарков на каждом магазине сети должен быть не менее 50 штук.

Опишите, как на Ваш взгляд, выглядит оптимальный процесс информирования и отчетности по проекту, который позволит достигать целей и соблюдать ограничения.

# Ответ:

## Добавим конкретики:

Предположим, что не все магазины участвуют в акции, а только 10 магазинов - это для упрощения моих размышлений.

А себестоимость  подарка например - 500 рублей.

И мы знаем, что всегда должно оставаться в магазине 50 штук - Неприкосновенный запас.

## Решение:

> Самый лучший способ в наши дни получать отчеты автоматически в мессенджер.
> 

Чтобы оперативно иметь доступ ко всей необходимой информации можно настроить Telegram-bot.

<aside>
📌 [t.me/GOLG_585_test_bot](https://t.me/GOLG_585_test_bot) - Бот работающий. Его можно открыть и понажимать кнопочки.

</aside>

Бот будет работать до 4 октября.

В случа если он не будет отвечать, напишите мне в телеграм [https://t.me/agafonova_ds](https://t.me/agafonova_ds)

![photo_2022-09-30_15-31-15.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f590e617-4708-4996-8449-ff34e847a163/photo_2022-09-30_15-31-15.jpg)

![photo_2022-09-30_15-31-17.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f89f7a91-bf9a-4ec9-a47e-5715aa1ea35e/photo_2022-09-30_15-31-17.jpg)

![photo_2022-09-30_15-31-16.jpg](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/099d7f55-2147-4ad2-8ae0-8b777c84c09c/photo_2022-09-30_15-31-16.jpg)

В основе бота лежит фейковая база. 

В реальности вся информация подтягивается из базы при помощи API.

В основе запросов могут быть на SQL или же  на Python и любой из ORM фреймворков, которые затем обращаются к СУБД.

Второй вариант более гибкий в плане формирования запросов.

<aside>
📌 Очень удобно,  в любой момент человек у которого есть доступ к боту может посмотреть необходимую информацию по любому магазину.
Необходимо только изначально наладить правиьную логику бота.

</aside>

В случае потребности можно добавить функции, которые будут выводить общее количество остатков, или же сегметрировать магазины по географии.

### Процесс информирования.

Также в телеграм можно отправлять уведомления в случае, когда ситуация выходит из подконтроля.

Введём некоторые переменные, для удобного обозначения:

- $balance$ - остаток подарков в магазине без учёта неприкосновенного запаса;
- $nz$ - остаток  неприкосновенного запаса
- $avg$  - среднее количество подаренных подарков за период (месяц)
- $days_{end}$ - количество дней до конца периода

Допустим на согласование доп. бюджета необходимо 7 дней.

И устоновим два стандартных алерта, которые будут нам сигнализировать, что стоит уделить внимание.

**1 алерт:** 

$M_1$ - средний количество подарков до конца периода

$$
M_1 =\dfrac{balance+nz}{days_{end}} 
$$

Если $M_1$ меньше чем avg, то это повод рассмотреть условия согласования дополнительно бюджета или перераспределение среди магазинов. 

> Возможно даже в этом случае лучше рассматривать скользящее среднее за небольшой период (Например за количество дней необходимых для согласования), чем просто $avg$
> 

**2 алерт:** 

Второй необходимый звоночек должен звенеть, когда начали дарить подарки из $nz$.

Поскольку это необходимое условие по заданию.