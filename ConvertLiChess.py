# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 21:26:29 2025

@author: Alchle
This program came about because I wanted to use the Lichess database of puzzles 
found here: https://database.lichess.org/#puzzles
However, I didn't like the position they put the database in. here is the note
from their website:
    FEN is the position before the opponent makes their move.
    The position to present to the player is after applying the first move to that FEN.
    The second move is the beginning of the solution. 
Thus, if it is Mate in 1 with white to move, the FEN is actually showing 
the previous position with black to move. The next move has to be taken
in order to put the board in the Mate in 1 situation. 

Took 17 seconds to process 554,059 mateIn1 puzzles
Took 120 seconds to re-write entire file to include the previous move (4,679,273 puzzles)
"""


#================================================
# SETUP =========================================
#================================================

import time

#Note slashes in file path are opposte of MS Windows
file_name = 'D:/lichess_db_puzzle.csv'
out_filenameText = 'D:/ALL.csv'
strTheme = "ALL"    #mateIn1, mateIn2, mateIn3, etc... List of Themes at bottom of code
                    #using "ALL" will process entire file
strPGNTitle = "Mate in 1"   # Only used if boolOutputPGNCol == True
boolDebug = False           # Set to True to show prints. Slows down drastically when processing full file 
valReadLinesCount = -1      # To run full file, set to -1
valWriteLinesCount = -1     # Stops after finding X puzzles with strTheme (-1 writes all)
boolOutputFile = True       # To save output to file, set to True
boolOutputPGNCol = False    # Save a column containin the PGN info for imports

#================================================
# DEFINING FUNCTIONS ============================
#================================================

# Function used to expand FEN
def FENexpand(strFEN):
    FENexpand = ""
    if boolDebug == True: print("Entered function and passed:" + strFEN)
    for f in strFEN:
        if f.isnumeric() == True:
            FENexpand = FENexpand + ("1"*int(f))
        else:
            FENexpand = FENexpand + f
    if boolDebug == True: print("leaving function as:" + FENexpand)
    return(FENexpand)
    
    
# Function used to condense FEN
def FENcondense(strFEN):
    if boolDebug == True: print("Entered function and passed:" + strFEN)
    #for t in FENfrom:
    FENcondense = strFEN.replace("11111111","8")
    FENcondense = FENcondense.replace("1111111","7")
    FENcondense = FENcondense.replace("111111","6")
    FENcondense = FENcondense.replace("11111","5")
    FENcondense = FENcondense.replace("1111","4")
    FENcondense = FENcondense.replace("111","3")
    FENcondense = FENcondense.replace("11","2")
    return(FENcondense)


# Function to convert a,b,c, to 1,2,3
def ConvertABC_to_123(strInput):
    if strInput == "a":
        return "1"
    elif strInput == "b":
        return "2"
    elif strInput == "c":
        return "3"
    elif strInput == "d":
        return "4"
    elif strInput == "e":
        return "5"
    elif strInput == "f":
        return "6"
    elif strInput == "g":
        return "7"
    elif strInput == "h":
        return "8"

#================================================
# START OF MAIN CODE ============================
#================================================
start = time.time()
countread = 0
countwrote = 0

#Open file where to save output
with open(out_filenameText , "a") as myfileOut:
    
    #open file to read (downloaded at https://database.lichess.org/#puzzles)
    #This is a huge file, around 800MB. This code will only process one line
    #at a time thereby not stressing your computer's memory by loading 
    #entire file at once.
    with open(file_name) as file:
        #Write headerline to file
        if boolOutputPGNCol == True:
            myfileOut.write("PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl,OpeningTags,NewFEN,NewMoves,PGNText\n")
        else:
            myfileOut.write("PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl,OpeningTags,NewFEN,NewMoves\n")
        
        #iterate each line and process
        for line in file:
           if boolDebug == True: print(line)
           
           #choose what Theme you want to save in output file (a.k.a. Filter)
           if ((strTheme in line) or (strTheme  == "ALL")) and (countread > 0):
               #myfileOut.write(line)
               
               #Remove the new line from line being read
               line = line.replace('\n', '').replace('\r', '')
               
               #split the current row in csv file into fields
               items = line.split(",")
               if boolDebug == True: print(items)
               
               PuzzleId=items[0]
               FEN=items[1]
               Moves=items[2]
               Rating=items[3]
               RatingDeviation=items[4]
               Popularity=items[5]
               NbPlays=items[6]
               Themes=items[7]
               GameUrl=items[8]
               OpeningTags=items[9]
               
               
               if boolDebug == True: print(Moves)
               if boolDebug == True: print("FEN = " + FEN)
               
               #separate FEN code into list
               #i.e. 4r3/1k6/pp3r2/1b2P2p/3R1p2/P1R2P2/1P4PP/6K1 w - - 0 35
               #     -> ['r1bqk2r', 'pp1nbNp1', '2p1p2p', '8', '2BP4', '1PN3P1', 'P3QP1P', '3R1RK1']
               FENEnding = FEN.split(" ",1)[1]
               FENlist = FEN.split(" ",1)[0].split("/")
               if boolDebug == True: print(FENlist)
               if boolDebug == True: print("FENEnding = " + FENEnding)
               
               #Determine the next move "from" and "to" rank/row and file/column
               #i.e. e5f6 means the next move is from e5 to f6 (piece type is not listed in move)
               #This will output valRankFrom = 5, valRankTo = 6, valFileFrom = e, valFileTo = f
               valRankFrom = Moves[1:2]
               valRankTo = Moves[3:4]
               valFileFrom = Moves[0:1]
               valFileTo = Moves[2:3]
               if boolDebug == True: print(valFileFrom + " -> " + ConvertABC_to_123(valFileFrom))
               if boolDebug == True: print(valRankFrom)
               if boolDebug == True: print(valFileTo + " -> " + ConvertABC_to_123(valFileTo))               
               if boolDebug == True: print(valRankTo)
               
               #Extract FEN, show the next move's corresponding rank's pieces: "from" and "to" ranks
               #Note: FEN is in reverse order with the first item being rank/row 8,
               #second item being rank 7, etc...
               #the 8- is becuase first rank/row is 7th index (0->7)
               #FEN format list 8th rank first, 7th rank second spot
               FENfrom = FENlist[8-int(valRankFrom)]
               FENto = FENlist[8-int(valRankTo)]
               if boolDebug == True: print("FENfrom = " + FENfrom)
               if boolDebug == True: print("FENto = " + FENto)
               
               #Expand FEN "from" and "to"
               #i.e. 3R1RK1 -> 111R1RK1 (which works with FEN format)
               FENfromExpanded = FENexpand(FENfrom)
               FENtoExpanded = FENexpand(FENto)                  
               if boolDebug == True: print("From Expanded = " + FENfromExpanded)
               if boolDebug == True: print("To Expanded = " + FENtoExpanded)
                              
               #Determine piece moved and Replaced in destination location from source rank/row
               pieceMoved = FENfromExpanded[int(ConvertABC_to_123(valFileFrom))-1:int(ConvertABC_to_123(valFileFrom))]
               if boolDebug == True: print("pieceMoved = " + pieceMoved)
               FENtoExpanded_New = FENtoExpanded[:int(ConvertABC_to_123(valFileTo))-1] + pieceMoved + FENtoExpanded[int(ConvertABC_to_123(valFileTo)):]
               if boolDebug == True: print("New To Expanded = " + FENtoExpanded_New)
               
               #Make source location empty (put a 1 in it's from location)
               FENfromExpanded_New = FENfromExpanded[:int(ConvertABC_to_123(valFileFrom))-1] + "1" + FENfromExpanded[int(ConvertABC_to_123(valFileFrom)):]
               if boolDebug == True: print("New From Expanded = " + FENfromExpanded_New)
               
               #Condense FEN 
               #i.e. pp111r11 -> pp3r2
               FENtoNew = FENcondense(FENtoExpanded_New)
               FENfromNew = FENcondense(FENfromExpanded_New)
               if boolDebug == True: print("FENfromNew = " + FENfromNew)
               if boolDebug == True: print("FENtoNew = " + FENtoNew)
               
               #Compile new FEN with the next chess move taken place so that mate in one is indeed the next move
               #i.e. 000Zo,4r3/1k6/pp3r2/1b2P2p/3R1p2/P1R2P2/1P4PP/6K1 w - - 0 35 (was whites turn, need to make it blacks turn)
               #This is a mate in 2, but LiChess lists the previous move, so blank mates in 2 shows up as whites turn with 3 turns to go
               #w -> b
               FENNew = ""
               strConc = "/" 
               for row in range(0,len(FENlist)):
                   if row == 7: strConc = ""
                   if row == 8-int(valRankFrom):
                       FENNew = FENNew + FENfromNew + strConc 
                   elif row == 8-int(valRankTo):
                       FENNew = FENNew + FENtoNew + strConc 
                   else:
                       FENNew = FENNew + FENlist[row] + strConc 
               #print("New FEN = " + FENlist[0] + "/" + FENlist[1] + "/" + FENlist[2] )
               if boolDebug == True: print("FENNew = " + FENNew)
               
               
               #Swap player turn and build
               if FENEnding[0:1] == "w": 
                   FENEndingNew = FENEnding.replace("w", "b")                
               else:
                   FENEndingNew = FENEnding.replace("b", "w")
               
               FENNew = FENNew + " " + FENEndingNew
               if boolDebug == True: print("FENEndingNew = " + FENEndingNew)
               if boolDebug == True: print("FENNew = " + FENNew)
               
               #Now that the first move in Moves has been made, erase it so show remaining moves
               NewMove = Moves.split(" ",1)[1]
               if boolDebug == True: print("NewMove = " + NewMove)
               
               
               #Add column containing the PGN info for other use
               PGNText = ""
               if boolOutputPGNCol == True:
                   #Determine who wins to add to PGN
                   if FENEndingNew[0:1] == "w": 
                       WhoWins = " (1-0)} *" 
                   else: 
                       WhoWins = " (0-1)}  *"
                   
                   PGNText = "[Event \"" + strPGNTitle + "\\\\" + GameUrl + "\"]" + \
                       "[FEN \"" + FENNew + "\"]" + \
                       "1. " + NewMove[0:2] + " {" + NewMove + WhoWins 
                   
                   if boolDebug == True: print("PGNText = " + PGNText)
               
               #Create final string to write to CSV file              
               newLine = PuzzleId +","+ \
                   FEN + "," + \
                   Moves + "," + \
                   Rating + "," + \
                   RatingDeviation + "," + \
                   Popularity + "," + \
                   NbPlays + "," + \
                   Themes + "," + \
                   GameUrl + "," + \
                   OpeningTags + "," + \
                   FENNew + "," + \
                   NewMove + "," + \
                   PGNText + "\n"
                   
               if boolDebug == True: print(newLine)              
               
               if boolOutputFile == True:
                   myfileOut.write(newLine)

               countwrote = countwrote + 1
           
           countread = countread + 1
           
           #To test code, set equal to 10 or so. This will stop after 10 lines
           #To run full file, set to -1
           #Conditions when to stop iterations
           if countread == valReadLinesCount:
               break
           
           if countwrote == valWriteLinesCount:
               break
    end =  time.time()
    print("Execution time in seconds: ",(end-start))
    print("No of lines read: ",countread)
    print("No of lines wrote: ",countwrote)

    file.close()

myfileOut.close()

# LIST OF THEMES IN LiCHESS
"""
advancedPawn
advantage
anastasiaMate
arabianMate
attackingF2F7
attraction
backRankMate
bishopEndgame
bodenMate
capturingDefender
castling
clearance
crushing
defensiveMove
deflection
discoveredAttack
doubleBishopMate
doubleCheck
dovetailMate
endgame
enPassant
equality
exposedKing
fork
hangingPiece
hookMate
hrts
interference
intermezzo
killBoxMate
kingsideAttack
knightEndgame
long
master
masterVsMaster
mate
mateIn1
mateIn2
mateIn3
mateIn4
mateIn5
middlegame
oneMove
opening
pawnEndgame
pin
promotion
queenEndgame
queenRookEndgame
queensideAttack
quietMove
rookEndgame
sacrifice
short
skewer
smotheredMate
superGM
trappedPiece
underPromotion
veryLong
vukovicMate
xRayAttack
zugzwang
"""

    
    
    
    
    
    
    
    
    
    
