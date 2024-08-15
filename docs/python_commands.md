# pyprototypr: Using Python Commands

Working with an actual programming language, if you're not a programmer, can be a bit intimidating. Hopefully, though, by the time you're looking at this section you will be somewhat comfortable with writing **pyprototypr** scripts and therefore already on your way to controlling the computer through a language.  The concepts and methods represented here are relatively small increments to what you are likely already know, but hopefully will give you more flexibility in terms of the way you write scripts without adding too much complexity. There are *not* essential but can be useful.

> If you already know the Python programming language, you can skip this section!

Most programming languages have the concept of **loops** and **if** statements.  These commands are used to control the behaviour of the program in some way.

## Loops

A loop represents a section of your script that you want to repeat a number of times. If you were doing a recipe, for example, it might say: *Add a cup of flour and add an egg and mix; add another cup of flour and add another egg and mix; add a third cup of flour and a third egg and mix*.  So this is really the set of actions that gets repeated three times. You could rephrase this in a different way. *Repeat three times: Add a cup of flour, add an egg, and mix*. The two parts of this statement represents what happens in a loop. The first part indicates how many times the loop happens, and the second part is the action, or set of actions, that need to be repeated.

In a Python, or **pyprototypr**, script, a loop can be set-up by using the following kind of statement:
```
for count in range(1, 4):
    add_egg()
    add_flour()
    mix()
```
In this case the first line is the loop set-up:

* the "for" indicates that we want to set-up a loop;
* the "range" part specifies how many times we want the loop to happen using a start and end value inside a pair of brackets (1 and 4 respectively);
* "count" stores what the current number of times that the loop has happened (for the very first time the value of count will be set to the start value of 1).

The line ends with `:` to show that it is expected that more lines will follow.

The lines immediately following this set-up line are all the actions that must happen each time. These lines must all be indented 4 spaces and lined up below each other to show they are part of the loop.  (*Note:* ignore the words used here; they are just to indicate the concept of actions ... practical examples are shown below!).

Once the action(s) have been carried out, the program goes back to the `for` line - this is where the "loop" concept comes from - to increase the `count` value and prepare to carry out the action(s) again.

It should be noted that when the `count` reaches the end value, it will stop right away and not process any of the action(s) again; so, in this example, the actions are only carried out 3 times.

In the case of **pyprototypr**, a loop can be used to draw an item a number of times; for example:
```
for count in range(1, 4):
    Circle(x=1, y=count)
```
Here the value of `y` for the Circle will be set to a different number every time the loop operates. For the first time it will have a value of 1 (one); the second time a value of 2 (two); and the third time value of 3 (three).  This means that the Circle will be drawn in three different `y` locations on the page.

You can combine the value of the count with other information to do more complex kinds of operations. In this next example, the values for `y` will be 0.5, 1.0 and 1.5 over the three iterations of the loop.
```
for y_location in range(1, 4):
    Circle(x=1, y=y_location*0.5)
```
Note that we have used a different word in place of the usual `count`.  It does not matter too much which word you use; so pick one that makes sense in terms of what you're trying to achieve by using it.

Multiple loops can be used to control different values. For example:
```
for y_location in range(1, 3):
    for x_location in range(1, 3):
        Circle(x=x_location, y=y_location)
```
Here the outer loop runs twice, setting values for both `x` and `y`.  The outer loop happens twice, and for each time it happens, the inner loop happens twice.  So there are actually four times (2 times 2) that the actions - in this drawing a Circle - are carried out.

The value of the loop count normally goes up by 1 each time; but you can set a third value for the `range` that is a different increment number. For example:
```
for count in range(1, 7, 2):
    Circle(x=1, y=count)
```
Here count takes on the values 1, 3 and 5; because the third value of 2 is added to count each time the loop operates.

## If Statements

And if statement is a way to allow the computer to make decisions based on the information available to  it.

All us of make similar decisions. When we are driving a vehicle along a road and we approach a traffic light, we evaluate the color of the traffic light and make a decision; if the light is green we carry on driving but if the light is red we come to a stop.

In a similar way we can set up a statement to allow the script to behave differently according to information that it has.

So an `if` statement will look something like this:
```
if color == green:
    keep_driving()
else:
    stop_driving()
```
You'll see that they are really two parts to the if. The first part is the condition that we are trying to evaluate - in this case what the value of the color is - and the second part is the alternative.  As with the loop, the statement ends with a : Followed by one or more lines that are all indented below each other; these represent the actions that are to be carried out in that part of the statement.

The statement itself that forms part of the `if`, is what is termed a "true or false" check.  This means that it's a comparison of some kind. In this case the script examines the value stored inside `color` and checks if it is equal to (the double-equals sign) the value of `green`. And because the script understands what is meant by `green` it can carry out this comparison.

Should the comparison be dealing with two values that are equivalant then the check is deemed to be correct or "true", and so the actions that are in the first part of the `if` are carried out - in this case the `keep driving` action - and the rest will be ignored. However, should the comparison be false, for example because the value stored in `color` is red or orange, then the second part of the if statement will be carried out - in this case the `stop driving` action.

An `if` statement can be used inside a loop, for example:
```
for count in range(1, 5):
    if count < 3:
        Circle(x=1, y=count)
    else:
        Rectangle(x=1, y=count)
```
Here, the script will either draw a Circle or a Rectangle depending on the value of `count`: if its less than than 3 (the `<` comparison is a "less than" check), then a Circle, otherwise if its 3 or more, then a Rectangle
.
