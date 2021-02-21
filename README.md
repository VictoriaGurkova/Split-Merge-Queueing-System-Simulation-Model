Study of a Split-Merge Queueing System with two demand classes and losses 
======

### Введение
Системы массового обслуживания (СМО) с 
делением и слиянием требований (Fork-Join Queueing Systems) 
представляют собой модели реальных систем с параллельной обработкой
(многопроцессорные системы, GRID-системы, MapReduce и т.д.). 
В таких системах поступающие для обработки требования делятся на более 
простые для обслуживания фрагменты, которые распределяются по системе, 
занимая выделенные для них ресурсы. 

После завершения обслуживания фрагменты 
освобождают выделенные им ресурсы, но исходное требование будет считаться 
обслуженным и покинет систему только после завершения обслуживания всех 
его фрагментов.

# 

### Описание модели
Split-merge система массового обслуживания состоит из M обслуживающих
приборов, двух очерей ограниченной вместимости c1 и c2 
соответственно с дисциплиной обслуживания FCFS. 

В систему обслуживания поступают два класса требований, 
время между интервалами поступления которых распределено по 
экспоненциальному закону с параметрами &#955;1 и &#955;2 соответственно. 
Требования первого класса поступают в первую очередь, 
требования второго класса — во вторую очередь.

![model](https://github.com/ViktoriaGurkova/Split-Merge-Queueing-System/raw/master/img/model.png)

Требование, поступающее на обслуживание, состоит из заданного 
числа фрагментов. В том случае, когда свободных приборов достаточно 
для обслуживания всех фрагментов требования, фрагменты 
одновременно занимают свободные приборы и начинают 
обслуживаться. Если приборов недостаточно для обслуживания 
требований первого или второго класса, требования поступают 
на ожидание в очередь. В связи с ограниченной вместимостью 
очередей, требования, не заставшие свободных мест в первой 
или второй очереди, теряются, то есть возвращаются обратно 
в источник. 

Предполагается следующая последовательность извлечения требований 
из очередей: если первая очередь не пуста и имеется достаточное 
количество свободных приборов, на обслуживание поступает 
требование первого класса, иначе, если вторая очередь не пуста, — 
требование второго класса. Таким образом, требования первого 
класса имеют приоритет по отношению к требованиям второго класса.

Длительность обслуживания фрагмента любого класса на приборе есть 
экспоненциально распределённая случайная величина с параметром 	&#956;.

Следует отметить, что фрагмент, обслуживание которого завершено, 
не освобождает обслуживающий прибор, а занимает (блокирует) его 
до момента, когда все родственные ему фрагменты, то есть фрагменты
одного и того же требования, не завершат своё обслуживание. 
Только после завершения обслуживания последнего фрагмента 
требование освобождает приборы и покидает систему.