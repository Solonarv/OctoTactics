CellWars
========

## Short description
A RTS without any units, or formal bases.

## Game environment
The game is played on a board divided into octogonal and square cells, which have different stats.

## Game mechanics
Each cell has a certain amount of energy and generates some over time. Cells may transfer this energy to others in range.

If transferring to an allied cell, this increases the target cell's energy.
If the target is enemy, its energy is reduced.
Cells may receive various upgrades that may periodically attack, reduce energy lost from enemy attacks, ...

## Victory conditions

Players can take over a cell by being the last one to hit them when their energy falls below 0.

Global loss conditions (exhaustive list):

 - If no cell on the game board belongs to them
 - If any other player wins before they do

Global win conditions (exhaustive list):

 - If no enemy cells remain
 - If all their opponents lose

Specific win conditions (_non_exhaustive list):

 - If they have conquered a certain number of cells
 - If they have not lost for a certain amount of time (vs. AI only)
 - If they have sustained a certain amount of cells for some time
 - If they have gained a certain amount of points, gained by accomplishing specific tasks

TL;DR: Conquer as many cells as you can to win (usually). There is only ever one winner per match.

## Game modes

### Player vs. AI
The player fights against one or more computer-controlled opponents.
The AI used is an evolution-tuned utility maximizer: It calculates the expected utility for each
of its possible actions and chooses the action that leads to the highest EU.
The weights used in the calculation of a game state's utility are tuned by a genetic algorithm.
The AI recalculates its options about once per second, or when either a transfer is changed or a cell changes owner.

### Player vs. Player (PvP)
Several players compete against on another.

The game may be hosted on any machine, including that of one of the players.
Some sort of network connection between the host and the players' machines will be required.

### AI vs. AI
Several AIs compete against one another. This mode exists mainly to allow competition between different custom
AIs.

### Co-op modes
All of the above modes have co-op versions, in which the participants may group into an arbitrary amount of teams
of arbitrary size. AI teams may be created by the game admin; they will be made up of a number of AI opponents
roughly equal to the average size of the player teams.

### Notes

 - AIs are not aware that they are playing against other AIs.
 - AIs run in a separate thread from the server, and may in fact run on another machine.

## Modding & Source code
The game was written from the ground up to support modding. Most behaviors are implemented through event buses, which means
that it is very easy to create mods that hook into that event system to accomplish various reactive tasks.
Cell Wars also features an extensive API, which allows modders to easily add features such as game modes or cell upgrades.

## Terms of Use

### What you buy
When you purchase Cell Wars, you do so as is. This includes any bugs, missing features or other shortcomings.
Purchasing gives you a code allowing you to download any version of the game (including future ones),
either as full source code or as optimized python files (.pyo). You may use this link to download the game
as often as you like\*, and install and use it on as many machines as you like. This code cannot be linked
to your person, and you may not distribute it to anyone. Keep it well, as it is the only way for you to obtain
a fresh copy of the game.

\* Unless the servers are down. If you download an excessive amoutn of copies, this may be your fault, and we'll
ask you to stop.

### The One Rule to Rule Them All
Do not distribute anything we've made, be it altered or not, without explicit written permission.

You are free to create content of any kind related to the game, and use it in any way that complies with the law in effect
where you live. This includes commercial use; you may e.g. sell a plugin a tool related to this game.
Anythign you make from scratch, as well as any modifications or plugins you've made, belong to you. We reserve the
right to demand tools or plugins to be removed if we see fit, and the final a´say as to what is or not a tool or plugin.
You may not mislead people into thinking your creation is in any way affiliated to or endorsed by us.
See the brand guidelines below.

### Privacy
Our web servers store your IP address for at most 48 hours.
We will also store the timestamps of all downloads, and the code used to access them.

Since we cannot associate the download codes with your person, we are unable to divulge or delete the data associated
with them. You may request removal of data pertaining to your current IP address as seen by our web servers via an
online form.

### Other
These TOU are subject to change at any time, without prior notice.

You are free to offer us suggestions, which will be assumed to be offered for free unless otherwise specified before
you communicating the suggestion to us.

If you have any legal questions not answered on this page, do not do it and ask us. 
Basically, don't mess with us and well leave you alone.

### TL;DR
Don't steal our stuff, don't pretend we endorse your stuff. Otherwise, do whatever you want.

~ Nicolas Stamm (Solonarv), DruideRappeur, anon$littleboy