### Flappy Bird with Python

Dev. by : Rad-wane

This game was not OOP based (only functions), the code has comments for clarity. 
It uses mainly `pygame`. Images used are in `images`, so are `sounds`. The font used is the one used in real *Flappy Bird* : `04B_19` with size 40.
`pygame` & `pygame.mixer` were initialized so that the game run smoothly :
* The screen dimensions choosen are : `576x1024`
* The framerate is set to 120
* `pygame.mixer` has the following initialization arguments : `frequency`=44100,`size`=16,`channels`=1,`buffer`=512

Pipes are generated every 1.2 second with random heights via a `user event`.
The bird rotate using `transform.rotozoom` in `pygame`, and animated using 3 images. 
There's a sound when : Colliding with the pipes or the screen boundary, the score is incremented and for each jump of the bird.

For further details, see the code : `Flappy_bird.py`

## Game play:

Using the spacekey, the bird goes up and down. Collisions between the bird and the pipes (with random heights), or the upper and lower boundary of the screen, are detected and result in the game over screen. 
The game over screen can be removed with the spacekey, a new game is lauched. 
The score of the game is incremented with 1 each time the bird goes between the pipes without touching them. 
A high score is updated each time accordinly and displayed in the game over screen. 

 
