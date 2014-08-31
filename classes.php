<?php
	class Question{
		public $Question;
		public $Id;
		public $Answers;
		public $SelectedAnswer;
		public $SubTitle;
		public $IsLastQuestion;
		public $IsFirstQuestion;
		public $IsImportant;
	}
	class Answer{
		public $Id;
		public $Text;
		public $Question;	
	}
	class Distribution{
		public $Id;
		public $Name;
		public $ChoosedBy = 0;
		public $ChoosedByQuestion = array();
		public $Description;
		public $License;
		public $Website;
		public $Place = 1;
		public $IsLastQuestion = false;
		public $ImageSource;
		public $TextSource;
	}


?>
