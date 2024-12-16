# from turtle import Turtle, Screen

# timmy = Turtle()            # Create a turtle object
# timmy.shape("turtle")       # Set the turtle shape 
# timmy.color("coral")          # Set the turtle color 
# timmy.forward(100)          # Move the turtle forward
# timmy.right(90)             # Turn the turtle right
# timmy.forward(100)          # Move the turtle forward
# timmy.right(90)             # Turn the turtle right
# timmy.forward(100)          # Move the turtle forward
# timmy.right(90)             # Turn the turtle right 
# timmy.forward(100)          # Move the turtle forward

# my_screen = Screen()    # Create a screen object
# my_screen.canvheight = 500  # Set the screen size
# my_screen.canvwidth = 500   # Set the screen size
# my_screen.exitonclick()     # Close the screen when clicked

import prettytable
table = prettytable.PrettyTable()
table.add_column("Pokemon Name", ["Pikachu", "Squirtle", "Charmander", "Bulbasaur", "Jigglypuff", "Gengar", "Pidgey", "Rattata", "Zubat", "Psyduck", "Meowth", "Abra", "Krabby", "Voltorb", "Geodude"])
table.add_column("Type", ["Electric", "Water", "Fire", "Grass", "Normal", "Ghost", "Normal", "Normal", "Poison", "Water", "Normal", "Psychic", "Water", "Electric", "Rock"])
table.align = "l"
table.sortby = "Pokemon Name"
print(table)
