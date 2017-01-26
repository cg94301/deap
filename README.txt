Use quantiacs.py27 env.

****

SCOOP:

conda install -c nickvandewiele scoop

****

Custom Types:
Since version 1.0, the types in STGP have to be real Python classes. This is expressed in the porting guide : http://deap.gel.ulaval.ca/doc/default/porting.html#strongly-typed-genetic-programming-stgp

This allows DEAP to take advantage of the Python object-oriented mechanisms. If your classes are only some form of constraints, simply define empty classes and use them as argument for the primitive set. For example

    class Row(object): pass
    # ...
    pset.addPrimtive(meanrow, [Row], float)

Regards,
Félix-Antoine

****

(quantiacs.py27) bash-3.2$ python spambase.py 
gen	nevals	avg   	std    	min	max
0  	100   	194.62	46.9178	107	303
1  	60    	228.23	39.7939	154	326
2  	72    	243.47	41.551 	139	335
3  	58    	260.79	40.5481	153	335
4  	56    	269.77	46.0428	104	335
5  	62    	271.1 	53.5572	84 	335
6  	49    	291.48	46.4096	105	335
7  	58    	298.76	41.219 	148	338
8  	64    	294.52	50.6964	112	336
9  	75    	285.11	56.4282	145	341
10 	65    	292.26	49.7296	142	341
11 	58    	301.09	44.5863	153	341
12 	62    	304.51	44.1079	148	341
13 	58    	292.75	54.1242	150	339
14 	52    	302.49	45.3558	113	339
15 	71    	302.89	47.4365	145	339
16 	55    	308.41	44.9077	146	344
17 	48    	305.94	47.3626	149	345
18 	53    	306.78	47.0711	134	345
19 	64    	309.8 	44.3935	143	345
20 	55    	306.25	43.1723	148	345
21 	67    	306.1 	40.5207	153	345
22 	56    	311.68	34.7594	221	345
23 	59    	310.58	38.8634	216	345
24 	55    	314.13	37.137 	154	345
25 	53    	314.27	37.8119	158	345
26 	59    	314.42	34.5422	227	345
27 	65    	309.93	41.0422	150	345
28 	59    	315.83	33.0699	216	345
29 	49    	313.98	43.5226	142	345
30 	61    	314.34	36.7223	217	345
31 	56    	325.77	27.7092	229	354
32 	64    	314.2 	47.0495	102	345
33 	59    	311.95	44.7478	148	345
34 	55    	322.55	33.9433	154	345
35 	50    	320.49	35.5307	165	345
36 	64    	316.69	37.7859	160	345
37 	59    	320.73	30.2569	222	345
38 	47    	324.41	29.1339	235	345
39 	61    	312.98	40.145 	154	345
40 	66    	319.05	31.825 	228	345
and_(lt(IN36, IN52), lt(protectedDiv(add(IN24, IN36), converter(IN24, 2.079212839244915)), IN52))
(quantiacs.py27) bash-3.2$ 

VICTORY!! Custom type was used in evolution.


****

SCOOP error. 

(quantiacs.py27) bash-3.2$ python -m scoop trader.py
[2016-10-19 09:15:33,996] launcher  INFO    SCOOP 0.7 2.0 on darwin using Python 2.7.12 |Anaconda 4.2.0 (x86_64)| (default, Jul  2 2016, 17:43:17) [GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2336.11.00)], API: 1013
[2016-10-19 09:15:33,996] launcher  INFO    Deploying 8 worker(s) over 1 host(s).
[2016-10-19 09:15:33,996] launcher  INFO    Worker d--istribution: 
[2016-10-19 09:15:33,996] launcher  INFO       127.0.0.1:	7 + origin
Launching 8 worker(s) using /bin/bash.

code:  and_(True, True)

...

code:  an
Traceback (most recent call last):

  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/site-packages/scoop-0.7.2.0-py2.7.egg/scoop/_control.py", line 150, in runFuture
d_(or_(True, False), and_(True, True))

    future.resultValue = future.callable(*future.args, **future.kargs)
  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/runpy.py", line 252, in run_path
    return _run_module_code(code, init_globals, run_name, path_name)
  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/runpy.py", line 82, in _run_module_code
code:  and_(or_(True, True), True)
code:  lt(sub(CLOSEARG, OPENARG), mul(95, OPENARG))
    mod_name, mod_fname, mod_loader, pkg_name)
  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "trader.py", line 296, in <module>
    pop, stats, hof, logbook = main()
  File "trader.py", line 290, in main
    _ , logbook = algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 10, stats, halloffame=hof)
code:  eq(66, 51)
  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/site-packages/deap/algorithms.py", line 160, in eaSimple
    for ind, fit in zip(invalid_ind, fitnesses):


  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/site-packages/scoop-0.7.2.0-py2.7.egg/scoop/futures.py", line 99, in _mapGenerator
    for future in _waitAll(*futures):
  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/site-packages/scoop-0.7.2.0-py2.7.egg/scoop/futures.py", line 360, in _waitAll
    for f in _waitAny(future):
  File "/Users/chrisg/opt/anaconda2/envs/quantiacs.py27/lib/python2.7/site-packages/scoop-0.7.2.0-py2.7.egg/scoop/futures.py", line 337, in _waitAny
    raise childFuture.exceptionValue
TypeError: coercing to Unicode: need string or buffer, Fitness found
code:  and_(eq(HIGHARG, OPENARG), not_(True))
code:  or_(lt(CLOSEARG, CLOSEARG), not_(False))

[2016-10-19 09:15:35,811] launcher  (127.0.0.1:51382) INFO    Root process is done.
[2016-10-19 09:15:35,842] launcher  (127.0.0.1:51382) INFO    Finished cleaning spawned subprocesses.

It works on spambase.py.
It works on spambase.customtype.py.

****

benchmark symbreg 400 generations:

running on single machine MAC. 

default: single process
> python symbreg.py
time:  24.991065979

multiprocess: 1 proc 4 threads, 8 proc single thread
> python symbreg.py
time:  15.1379599571

scoop: 9 processes 4 threads each
> python -m scoop symbreg.py
time:  43.6128218174


****

Console.

> python trader.console.py
> main()

Opens embedded console. Call main() to run program.


> IPython
> run trader.py

or

> import trader
> trader.main()


