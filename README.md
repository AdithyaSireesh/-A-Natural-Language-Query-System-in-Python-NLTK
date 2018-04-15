# -A-Natural-Language-Query-System-in-Python-NLTK
In this project, I used Python2 and NLTK to construct a system that reads simple facts and then answers questions about them. You can think of it as a simple form of both machine reading and question answering. In the real world, such systems read large amounts of text (e.g. Wikipedia or news sites), populate database with facts learned from that text, and use the database to answer general knowledge questions about the world.3 
The completed system enables dialogues such as the following:
  
  $$ John is a duck.
  
       OK
       
  $$ Mary is a duck.
  
       OK
       
  $$ John is purple.
  
       OK
       
  $$ Mary flies.
  
       OK
       
  $$ John likes Mary.
  
       OK
       
  $$ Who is a duck?
  
       John  Mary
       
  $$ Who likes a duck who flies?
  
       John
       
  $$ Which purple ducks fly?
       None
       
