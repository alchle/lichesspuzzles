# lichesspuzzles
Convert lichess puzzles to include the previous move

Hello all, just sharing that I found a post https://lichess.org/forum/general-chess-discussion/hello-chess-friends-can-anyone-do where it listed what I wanted, but no solution was created.  

I was looking at printing some puzzles from https://database.lichess.org/#puzzles but found that all the puzzles were not in the "proper position."  Meaning, it was mate in 1 for white, but the FEN was at blacks move, before it was white's turn to mate in 1 move.  That is by design by lichess per their website which states:

"FEN is the position before the opponent makes their move.
The position to present to the player is after applying the first move to that FEN.
The second move is the beginning of the solution. "

But this bugged me, so I wrote a python script (version 3.12) that applies the next move, recreates the FEN to reflect it.  Thus, when it says it is white's mate in 1, it indeed shows the board with white's move and check mate in 1. [probably not the most eligant code writing, but it works.  I haven't done much python]

lichess format:
000Zo	4r3/1k6/pp3r2/1b2P2p/3R1p2/P1R2P2/1P4PP/6K1 w - - 0 35	e5f6 e8e1 g1f2 e1f1	1353	75	86	627	endgame mate mateIn2 short	https://lichess.org/n8Ff742v#69

My new format (Added the last two fields: NewFEN and New Moves
000Zo	4r3/1k6/pp3r2/1b2P2p/3R1p2/P1R2P2/1P4PP/6K1 w - - 0 35	e5f6 e8e1 g1f2 e1f1	1353	75	86	627	endgame mate mateIn2 short	https://lichess.org/n8Ff742v#69		4r3/1k6/pp3P2/1b5p/3R1p2/P1R2P2/1P4PP/6K1 b - - 0 35	e8e1 g1f2 e1f1

The script will also generate PGN if so desired into another column. It's not the full game of course, but I used it here: https://pgn2pdf.com/  to genereate pdf files of the puzzles. That is a neat website.
