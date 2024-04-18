# Base Quantum Game

_Prepared by Abuzer Yakaryilmaz (April 2024)_

We will develop a quantum game but keep it very simple to give enough room for building on top of it.

Let's check it together first!

Now, we discuss its details and features.

**Two screens**

There are two screens. So, it might be helpful to define the half of heigth as a new constant variable.

```
HALF_HEIGHT = SCREEN_HEIGHT // 2
```

We draw a line between two screens.

```
# draw a line on the screen with specified color and starting and ending coordinates, from (x1,y1) to (x2,y2)
pygame.draw.line(screen, (0, 255, 0), (0, HALF_HEIGHT), (SCREEN_WIDTH, HALF_HEIGHT))
```

**Restrict player within its screen**

A photonic ship can be in up or down screen, but, it should not leave its screen while classical.

_In my code, I defined "allowable_top" and "allowable_bottom" variables for the player to make calculations easily._

After applying NOT operator, a photonic ship jumps into the other screen with the same position. So, we should keep the track of the screen that the photonic ship is in.

We can use a variable to keep the screen of the player. Alternatively, we can check if "top" value of the player is in the up screen or down screen. 

The following variable can be read and set:

```
player.rect.left
player.rect.top
```

**Accessing global variable**

To access a global variable within a method, we should explicitly specify this as below:

```
global_variable = 45

def my_method():
  global global_variable
  ...
```

Otherwise, we can get an error or use wrong values.

**Superposition of the player**

After applying HADAMARD operator, the photonic ship enters into a superpostion: Two photonic ships appear at the same positions of both screen.

Thus, we should create another player and position it accordingly.

**Quantum world**

While in superpostion, the photonics ships do not move.

Instead, the enemies move up and down with the up and down arrow keys, respectively. Then, the "update" method of "Enemy" should be modified accordingly.

We should allow the enemies to move beyond the borders. We can assume that top and bottom are connected (circular), and so once off from the top, they can appear from the bottom, and vice versa. They can also cross the middle line.

The previous enemy speed interval might be too challenging while playing, and so, we can limit the max speed.

_In my code, I defined "SPEED_MIN = 5" & "SPEED_MAX = 10"._

**Measurement**

While in superposition, any enemy hitting the player forces the photonic ship to be measured. So, the photonic ship collapses into one of the screen with the equal probablity.

If the enemy is in the same screen with the collopased the ship, the game is over. Otherwise, the game is continued as a single classical ship.

**Quantum operators**

Quantum operators are applied randomly while the game is ongoing. 

In the infinite loop, for example, we pick a number between 0 and 300:
- if the result is 100 or 200, we apply NOT operator.
- if the result is 150, we apply HADAMARD operator.

Remark that, while in a superposition, there is no sense to apply NOT operator.

On the other hand, while in a superposition, a second HADAMARD can be applied, and so, the ship becomes classical and returns the position just before the first HADAMARD.

_In my code, I defined "player" and "twin_player" when entering a superposition to keep their tracks easily._

**Screen messages**

It will be good to inform the player when a quantum operator or a measurement is applied.

It will also be good to show these messages for example for one second before the next frame.

You may use different colors for different type of messages.

**Possible extensions/modifications**

We will discuss possible extensions and modifications to make the game more interesting and playable.
