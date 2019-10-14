import linda
linda.connect()

blog = linda.TupleSpace()
linda.universe._out(("Microblog",blog))

blog = linda.universe._rd(("MicroBlog",linda.TupleSpace))[1]

blog._out(("Maria", "medica", "capita do time de volei na escola"))
blog._out(("Maria", "advogada", "faixa preta no karate"))
blog._out(("Maria", "programadora", "campea do time de natacao do ensino medio"))
blog._out(("Maria", "advogada", "diagnostico: sedentaria"))

t1 = blog._rd(("Maria", "advogada", str))

print(t1)

blog._in(("Maria", "advogada", "diagnostico: sedentaria"))

t1 = blog._rd(("Maria", "advogada", str))

print(t1)