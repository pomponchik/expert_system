# expert_system: логический движок


Движок представляет собой [экспертную систему](https://en.wikipedia.org/wiki/Expert_system) для работы с [логикой высказываний](https://en.wikipedia.org/wiki/Propositional_calculus). Он умеет делать автоматические выводы на основе переданных ему логических правил, а также, к примеру, выявлять в них противоречия.

- [**Входные данные**](#входные-данные).
- [**Поддерживаемые операции**](#поддерживаемые-операции).
- [**Алгоритм**](#алгоритм).
- [**Формат вывода**](#формат-вывода).
- [**Интерактивный режим**](#интерактивный-режим).


## Входные данные

Путь к файлу с правилами должен быть передан как аргумент при вызове скрипта, вот так:

```bash
$ python3 expert_system.py examples/example_input.txt
```

Сам файл должен выглядеть примерно так:

```
# this is a comment$
# all the required rules and symbols, along with the bonus ones, will be
# shown here. spacing is not important
C => E # C implies E
A + B + C => D # A and B and C implies D
A | B => C # A or B implies C
A + !B => F # A and not B implies F
C | !G => H # C or not G implies H
V ^ W => X # V xor W implies X
A + B => Y + Z # A and B implies Y and Z
C | D => X | V # C or D implies X or V
E + F => !V # E and F implies not V
A + B <=> C # A and B if and only if C
#A + B <=> !C # A and B if and only if not C
=ABG # Initial facts : A, B and G are true. All others are false.
# If no facts are initially true, then a simple "=" followed
# by a newline is used
?GVX # Queries : What are G, V and X ?
```

Все, что в строке находится правее диеза ("#") - игнорируется интерпретатором. Заглавные буквы латинского алфавита представляют переменные для логических констант (TRUE и FALSE).

Строки делятся на три типа, следующих строго друг за другом:
- Правила, преимущественно в формате [импликаций](https://en.wikipedia.org/wiki/Material_conditional).
- Исходные факты. Строка, которая их содержит, должна начинаться с символа "=". Все перечисленные здесь факты инициализируются как TRUE, остальные по умолчанию - FALSE, если иное не следует из исходных фактов и примененных к ним правил.
- Запросы. Строка должна начинаться со знака вопроса.

В случае нарушения формата файла, будет напечатана ошибка с указанием типа ошибки и номера строки.


## Поддерживаемые операции

Правило - это [булевая функция](https://en.wikipedia.org/wiki/Boolean_function). Операцией верхнего уровня в ней должна быть импликация или эквиваленция, все прочие операции будут проигнорированы.

Доступны следующие операции (в порядке понижения приоритета):

- "(" и ")" для обозначения приоритетов. Пример: ```A + (B | C) => D```.
- "!", обозначает приставку [НЕ](https://en.wikipedia.org/wiki/Negation). Пример: ```!B```.
- "+", обозначает [конъюнкцию](https://en.wikipedia.org/wiki/Logical_conjunction). Пример: ```A + B```.
- "|", обозначает [дизъюнкцию](https://en.wikipedia.org/wiki/Logical_disjunction). Пример: ```A | B```.
- "^", обозначает [исключающее ИЛИ](https://en.wikipedia.org/wiki/Exclusive_or). Пример: ```A ˆ B```.
- "=>", обозначает [импликацию](https://en.wikipedia.org/wiki/Material_conditional). Здесь важно различить два вида импликации. Импликация верхнего уровня должна быть строго одна, она используется программой для связывания логических выражений и построения выводов. Пример такой импликации: ```A + B => C```. Также импликация может использоваться в качестве обычного логического оператора, для этого она должна быть заключена в скобки (чтобы ее приоритет был искусственно повышен): ```(A => B) => C```.
- "<=>", обозначает [эквиваленцию](https://en.wikipedia.org/wiki/Logical_equality). По аналогии с импликацией, может быть двух уровней: на верхнем преобразуется в две зеркальных импликации, а на нижнем обрабатывается как обычная логическая операция. Примеры: ```A + B <=> C```, ```(A <=> B) <=> C```.

Как левая, так и правая части выражения могут быть составными. Для удобства вычислений левая часть по возможности упрощается и в дальнейших операциях используются одно или несколько производных уравнений.


## Алгоритм

Основой алгоритма является [обратный поиск](https://en.wikipedia.org/wiki/Backward_chaining) (он же - обратное связывание или обратная индукция). По сути это вариация вокруг обычного [обхода графа в глубину](https://en.wikipedia.org/wiki/Depth-first_search).

Каждое уравнение представляет собой дерево, каждой нодой которого является какая-то логическая операция или переменная. Мы последовательно обходим ноды с операциями, пока не натыкаемся на ноду с переменной. Если мы уже встречали ее раньше, значение подгружается из кэша, в противном случае мы его выясняем. В процессе выяснения нам может понадобиться вычислить другую переменную, и так далее.

Прежде, чем делать все эти операции, в памяти нужно создать граф, каждая нода которого соответствует одной переменной из исходного файла. В каждой ноде хранятся относящиеся к ней выражения, то есть те, где соответствующая переменная фигурировала справа от оператора импликации. Также там хранятся базовые значения, если они были переданы.

Чтобы получить из исходного текста выполняемые выражения, используются базовые приемы работы с такого рода текстами:

- [Токенизация](https://en.wikipedia.org/wiki/Lexical_analysis).
- Создание [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree).
- Преобразование AST в [семантический граф](https://en.wikipedia.org/wiki/Abstract_semantic_graph).


## Формат вывода

Результат работы передается в стандартный вывод. Вызвав программу так:

```bash
$ python3 expert_system.py examples/example_input.txt
```

... мы получим примерно такое решение:

```
X = TRUE from expression:
	((V)^(W))=>(X)
V = TRUE from expression:
	(!((E)+(F)))=>(V)
G = TRUE (initialization fact)
```

Как видим, для каждого запрошенного факта указывается как его значение, так и источник, откуда оно было получено. В настоящий момент рекурсивный вывод источника не поддерживается, однако может быть добавлен позднее.

В случае обнаружения противоречия в исходных данных, программа также сообщит об этом и прекратит работу.


## Интерактивный режим

Команды в экспертную систему также можно подавать в интерактивном режиме. Для этого скрипт нужно запустить без аргументов. В этом случае не важен порядок подачи строк, их назначение будет определяться по содержимому.

Кроме того, в интерактивном режиме доступна возможность назначать отдельным переменным алиасы. Синтаксис выглядит примерно так:

```
ALIAS A = "lol kek cheburek"
"lol kek cheburek" + B => C
```
