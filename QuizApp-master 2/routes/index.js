"use strict";

let express = require("express");
let router = express.Router();
let path = require("path");

//importing Database module
let database = require(path.join("..", "./Database"));

//importing Session module
let session = require("express-session");
//Creates a session
router.use(
  session({
    resave: true,
    saveUninitialized: true,
    secret: "SECRETSESSION",
    cookie: { maxAge: 60000 }
  })
);
//Variable for holding any session assigned later
let sess;

//Question Answer Set Holder
let set;

/* GET home page. */
router.get("/", function(req, res) {
  //Checks if already a logged session of user exists , else takes to login page
  if (sess) {
    //Directs to Main Bullseye Page
    res.redirect("/quizmain");
  } else {
    //res.render('index', { title: 'Express' });
    res.sendFile(path.join(__dirname, "..", "/public/html/login.html"));
    //res.sendFile(path.join('..','/html/login.html'));
  }
});

/* GET Login page. */
router.get("/login", function(req, res) {
  res.redirect("/");
});

/* POST Login Action page. */
router.post("/loginaction", function(req, res) {
  let loginDetails = req.body; //req.body is a json object containing username and password

  //Checking existence of loginDetails in database
  database.login(loginDetails, function(err, validDetails) {
    //Condition for valid Login data
    if (validDetails) {
      //validDetails consist of ---> { firstname,lastname,username,password }

      //assigns a session for a user
      sess = req.session;

      //stores validDetails of user in session
      sess.userDetails = validDetails;
      //console.log(sess.userDetails.firstname);

      res.redirect("/quizmain");
    } else {
      //Asks to Login on failing condition above
      res.send(
        '<div align="center">Invalid Login , Please Re-Enter Details or Register a New Account</div>'
      );
    }
  });
});

/* GET Register page. */
router.get("/register", function(req, res) {
  //Checks if already a logged session of user exists , else takes to login page
  if (sess) {
    res.redirect("/quizmain");
  } else {
    res.sendFile(path.join(__dirname, "..", "/public/html/register.html"));
  }
});

/* POST Register page. */
router.post("/registeraction", function(req, res) {
  let regDetails = req.body; //req.body is a json object containing username and password
  database.register(regDetails, function(decide) {
    //checks the value if username already exists
    if (decide == "success") {
      //Registration Successful!!
      res.redirect("/quizmain");
    } else {
      //if user already exists in database , asks to login
      res.send(
        '<div align="center">User already exists , Please <br><a href="/login">Click Here To Login</a></div>'
      );
    }
  });
});

/* GET Bullseye Main page. */
router.get("/quizmain", function(req, res) {
  //Condition for Existing Session
  if (sess) {
    res.sendFile(path.join(__dirname, "..", "/public/html/quizmain.html"));
  } else {
    res.send(
      '<div align="center">  Please Login to Play Quiz  <br><a href="/login">Login Here</a></div>'
    );
  }
});

/* GET instructions page. */
router.get("/instructions", function(req, res) {
  //Checks if already a logged session of user exists , else takes to login page
  if (sess) {
    res.sendFile(path.join(__dirname, "..", "/public/html/instructions.html"));
  } else {
    res.send(
      '<div align="center">  Please Login to Play Quiz  <br><a href="/login">Login Here</a></div>'
    );
  }
});

/* GET Scores page. */
router.get("/scores", function(req, res) {
  //Checks if already a logged session of user exists , else takes to login page
  if (sess) {
    res.sendFile(path.join(__dirname, "..", "/public/html/scores.html"));
  } else {
    res.send(
      '<div align="center">  Please Login to Play Quiz  <br><a href="/login">Login Here</a></div>'
    );
  }
});

/* POST Scores page. */
router.post("/scoreset", function(req, res) {
  //Code for retrieving score Details from DB and sending them in JSON type as response
  database.getScores(function(data) {
    res.json(data);
  });
});

/* GET Topics page. */
router.get("/topic", function(req, res) {
  //Checks if already a logged session of user exists , else takes to login page
  if (sess) {
    res.sendFile(path.join(__dirname, "..", "/public/html/topic.html"));
  } else {
    res.send(
      '<div align="center">  Please Login to Play Quiz  <br><a href="/login">Login Here</a></div>'
    );
  }
});

/* POST Topic selection action. */
router.post("/topicselect", function(req, res) {
  let category = req.body.topic;
  console.log(req.body);
  database.questionsFromDB(category, function(qaSet) {
    //assigning "qaSet" to global variable "set" to send json value of "set" variable in another GET Request (/jsonset)
    set = qaSet;
  });

  //Directing to Question-Answer Display page
  res.sendFile(path.join(__dirname, "..", "/public/html/questionpage.html"));
});

/* GET Request for JSON (Question-Answer) Set */
/*router.get('/jsonset', function(req, res, next) {
  //res.json(set);
});*/

/* POST Request for JSON (Question-Answer) Set */
router.post("/jsonset", function(req, res) {
  res.json(set);
});

/* GET Request for score updation */
router.post("/scoreupdate", function(req, res) {
  //Collecting name of user from session variable , and retrieving score from body
  let name = sess.userDetails.firstname;
  //formatting score to number
  let score = req.body.score.split("/")[0];

  //Combining (name,score) ---->  [name,score] Array
  let scoreSet = [];
  scoreSet.push(name);
  scoreSet.push(score);

  //sedning to database
  database.scoreupdate(scoreSet);
  res.sendFile(path.join(__dirname, "..", "/public/html/acknowledge.html"));
});

/* GET Request for JSON (Question-Answer) Set */
router.get("/questionreview", function(req, res) {
  //Checks if already a logged session of user exists , else takes to login page
  if (sess) {
    res.sendFile(
      path.join(__dirname, "..", "/public/html/questionreview.html")
    );
  } else {
    res.send(
      '<div align="center">  Please Login to Play Quiz  <br><a href="/login">Login Here</a></div>'
    );
  }
});

/* GET Logout page. */
router.get("/logout", function(req, res) {
  //destroys any session present
  req.session.destroy(function(err) {
    if (err) {
      console.log(err);
    }
  });

  //redirects to login page
  res.redirect("/login");
  //removes any session value in this Variable
  sess = null;
});

module.exports = router;
