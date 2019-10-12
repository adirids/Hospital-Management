"use strict";

let mysql = require("mysql");
let Database = {};

Database.configure = function() {
  //Database Configuration
  let connection = mysql.createConnection(
    {
      host: "localhost",
      user: "root",
      password: "12345",
      database: "quizdb"
    },
    function() {
      console.log("hello connection"); // eslint-disable-line
    }
  );
  connection.connect();

  //return Configuration connection
  return connection;
};

Database.login = function(loginDetails, done) {
  //Calling Configuration
  let connection = this.configure();

  //Retrieving login details from database
  let query = "select * from users where username='" +
    loginDetails.un +
    "' && password='" +
    loginDetails.pw +
    "'";
  connection.query(query, function(err, rows) {
    if (err) throw err;
    connection.end();

    //Checks if any usernames are returned with "loginDetails.un" name && "loginDetails.pw" password
    if (rows[0]) {
      done(err, rows[0]);
    } else {
      done(err, null);
    }
  });
};

Database.register = function(regDetails, done) {
  //Calling Configuration
  let connection = this.configure();
  //checks if user with username already exists
  connection.query(
    "select * from users where username=?",
    [regDetails.un],
    function(err, rows) {
      if (err) throw err;

      //if not exists enter details into database
      if (!rows[0]) {
        //Entering Details into Database
        console.log(!rows[0]);
        let query = "insert into users (firstname,lastname,username,password) values(?,?,?,?)";
        connection.query(
          query,
          [regDetails.first, regDetails.last, regDetails.un, regDetails.pw],
          function() {
            connection.end();
          }
        );
        done("success");
      } else {
        //callback return call
        done(null);
      }
    }
  );
};

Database.questionsFromDB = function(category, done) {
  //Calling Configuration
  let connection = this.configure();
  category = category.toLowerCase();
  connection.query(
    "select question,option1,option2,option3,option4 from questions where category=? ORDER BY RAND() LIMIT 10",
    [category],
    function(err, rows) {
      if (err) throw err;
      connection.end();
      //console.log(rows);
      let qaSet = { quizlist: rows };
      //console.log(set);
      done(qaSet);
    }
  );
};

Database.scoreupdate = function(scoreSet) {
  //Calling Configuration
  let connection = this.configure();
  connection.query(
    "select fname,score from userscores where fname=?",
    [scoreSet[0]],
    function(err, rows) {
      if (err) throw err;
      //console.log(scoreSet[1]);
      if (rows[0] && rows[0].score < scoreSet[1]) {
        connection.query(
          "update userscores set score=? where fname=?",
          [scoreSet[1], scoreSet[0]],
          function() {
            connection.end();
          }
        );
      } else if (!rows[0]) {
        connection.query(
          "insert into userscores (fname,noofquestions,score) values(?,?,?)",
          [scoreSet[0], 10, scoreSet[1]],
          function() {
            connection.end();
          }
        );
      }
      return;
    }
  );
};

Database.getScores = function(done) {
  //Calling Configuration
  let connection = this.configure();
  connection.query(
    "SELECT fname,score from userscores order by score desc",
    function(err, rows) {
      if (err) throw err;
      connection.end();

      done(rows);
    }
  );
};

module.exports = Database;
