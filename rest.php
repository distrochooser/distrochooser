<?php
	/**
	 * this file contains the program entry point
	 * @file
	 * @author  squarerootfury <me@0fury.de>	 
	 *
	 * @section LICENSE
	 *
	 * This program is free software; you can redistribute it and/or
	 * modify it under the terms of the GNU General Public License as
	 * published by the Free Software Foundation; either version 3 of
	 * the License, or (at your option) any later version.
	 *
	 * This program is distributed in the hope that it will be useful, but
	 * WITHOUT ANY WARRANTY; without even the implied warranty of
	 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	 * General Public License for more details at
	 * http://www.gnu.org/copyleft/gpl.html
	 *
	 * @section DESCRIPTION
	 *
	 * System entry point
	 **/
	
	require_once("./Includes/LDC.class.php");	
	require_once("./Includes/DB.class.php");
	if (!isset($_POST["method"]) || !isset($_POST["args"])){
		Abort();
	}
	$method = $_POST["method"];
	$args = json_decode($_POST["args"]);
	$l = $_POST["lang"];
	if (!isset($_POST["lang"]))
		exit();
	$ldc = new \LDC($l);
	if (!method_exists($ldc,$method) || empty($method)){
	 	$ldc->Abort();
	}
	else{
		echo call_user_func_array(array($ldc,$method), array($args));
	}
	
?>