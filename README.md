# Ray Casting
This is a ray casting test, but it might turn into a game. This uses Pygame to draw things onto the screen. To run the program, run the `ray_casting.py` file.

**Possible improvements:**

- [x] Add controls to move ray casting start point
- [x] Rotate direction of ray casting in direction of player movement while moving
- [x] Randomise walls to create diverse scenarios
- [ ] Make the walls solid so that the player can't pass through them
    - [ ] If this is the case, then we need to check whether the drawn lines create an enclosed polygon. If they do, then we need to know which lines are creating the polygon to make that area reachable. By randomising only one of those lines, the enclosed polygon can't be enclosed anymore, thus making it reachable. Some useful information: <https://stackoverflow.com/a/14333511> (graph theory!) :D
- [ ] Score tally
- [ ] Player, wall, and object sprites
- [ ] Background image
- [ ] Game mechanics to make it more interesting
    - [ ] Maybe have a shop to purchase a larger FOV or further view distance
    - [ ] Have an in-game currency (not using real money)
    - [ ] Could have high scores which would give extra rewards if you get a high score
    - [ ] Adding objects in random empty locations to be found
        - [ ] Each object has a point amount with it, the more you collect the bigger the point amount gets
        - [ ] Could make the scoring based on how many points you get, or based on the number of objects you collect, or the time you stay alive
    - [ ] A scoreboard that saves your 5 best attempts and 1 worst attempt (maybe using a database to store it)
        - [ ] It can store the date and time you achieved it, and the amount of time you took or the highest level you got to (depends how the game works)
    - [ ] Some NPCs that chase you around and if they get you then you lose a life
        - [ ] You might have 3 lives but you can purchase more that are used in the next game only (one-time use)
        - [ ] The NPCs get faster as you progress further to make it more difficult (could also increase the number of NPCs chasing)
- [ ] Could potentially make it so that the rays are facing the mouse cursor but the ray start point is controlled by the keyboard
