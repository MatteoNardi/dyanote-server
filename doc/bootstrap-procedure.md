# UPDATE PROCEDURE
|  GET /users/91.matteo@gmail.com/bootstrap?since=41000
|  
|  Return list of notes which changed since the last time bootstrap was called (41000)
|  { 
|       time: 42000,
|       root: 'Full root note...'
|       changes: [
|           { id: 2341, change: 41000 },
|           { id: 2342, change: 41023 },
|           { id: 2343, change: 41020 },
|           { id: 2344, change: 41034 }
|       ],
|   }
|  If we never syncronized or we have just logged in, do not set "since" parameter: we get list of all notes.
|  
|  For each note returned by server
|      if server timestamp is newer, mark it
|  Download marked notes
|  GET /notes?limit=234;123;1231;123;123;123
|  Update our notes
|  

