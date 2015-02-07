<?php
	class DB{		
		//TODO: Escape...
		public  $conn;	
		public function __construct(){
			$server   = 'mysql:dbname=;host=localhost; port=3333';
			$user     = '';
			$password = '';
			$options  = array
			            (
			              PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8',
			            );
			$this->conn   = new PDO($server, $user, $password, $options);
		}			
	}
?>