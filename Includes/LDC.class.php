<?php
	define("__LDC_VERSION__","2.0");
	define("__LDC_HOME__","http://distrochooser.0fury.de");
	class LDC{		
		private $db;
		private $lang;

		public function __construct($lang){
			$this->db = new \DB();

			$this->lang = trim($this->db->conn->quote($lang),"'");//$lang;
		}
		public function GetVersion(){
			return $this->Output(__LDC_VERSION__);
		}
		public function Output($value){
			return json_encode($value);
		}
		public function Abort(){
			header("HTTP/1.1 403 Forbidden");
			exit;
		}
		public function GetSystemVars(){
			$query = "Select Text,Val from dictSystem where LanguageId = ".$this->lang;
			$stmt = $this->db->conn->query($query);
			$result = $stmt->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($result);
		}
		public function GetDistributions(){
			$result = array();
			$query = "Select d.Id,d.Name,d.Homepage,d.Image, (
			Select dd.Description from dictDistribution dd where  dd.DistributionId = d.Id and dd.LanguageId = ".$this->lang." limit 1
			) as Description,d.ImageSource,d.TextSource from Distribution d";
			$stmt = $this->db->conn->query($query);
			$distros = $stmt->fetchAll(PDO::FETCH_CLASS);				
			foreach ($distros as $key => $value) {
				$distro = new \StdClass();
				$distro->Id = $value->Id;
				$distro->Name = $value->Name;
				$distro->Homepage = $value->Homepage;
				$distro->Image = $value->Image;
				$distro->Description = $value->Description;
				$distro->ImageSource = $value->ImageSource;
				$distro->TextSource = $value->TextSource;
				//Find out Answers for this distro
				$query = "Select * from AnswerDistributionRelation adr where adr.DistributionId = ".$distro->Id;
				$relations = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
				if (!empty($relations)){
					foreach ($relations as $k => $relation) {
						$distro->Answers[] = $relation->AnswerId;
					}
				}
				else{
					$distro->Answers = array();
				}		
				$query = "Select * from Media med where med.DistroId = ".$distro->Id;
				$mediaArray = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
				if (!empty($mediaArray)){
					foreach ($mediaArray as $k => $media) {
						$distro->Media[] = $media;
					}
				}
				else{
					$distro->Media = array();
				}	
				$result[] = $distro;		
			}
			return $this->Output($result);
		}
		public function GetQuestions(){
			$result = array();
			$query = "Select q.Id,q.OrderIndex, dq.Text,dq.Help from Question q INNER JOIN dictQuestion dq
			ON LanguageId = ".$this->lang." and QuestionId= q.Id order by q.OrderIndex";
			$stmt = $this->db->conn->query($query);
			$questions = $stmt->fetchAll(PDO::FETCH_CLASS);		
			//return $this->Output($questions);	
			foreach ($questions as $key => $value) {
				$question = new \StdClass();
				$question->Id = $value->Id;
				$question->OrderIndex = $value->OrderIndex;
				$question->Text = $value->Text;
				$question->Help = $value->Help;	
				$query = "Select a.Id,(
				Select da.Text from dictAnswer da where da.AnswerId = a.Id and da.LanguageId = ".$this->lang."
				)as Text from Answer a where a.QuestionId = ".$question->Id;
				$answers = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
				$question->Answers = $answers;
				$result[] = $question;						
			}
			return $this->Output($result);
		}
		public function AddResult($distros){		
			if (count($distros) == 0)
				return;
			$query = "Insert into Result (Date) Values(CURRENT_TIMESTAMP)";
			$stmt = $this->db->conn->prepare($query);
			$stmt->execute();
			$id = $this->db->conn->lastInsertId();	
			foreach ($distros as $key => $value) {				
				$query = "Insert into ResultDistro (DistroId,ResultId) Values(?,?)";
				$stmt = $this->db->conn->prepare($query);
				$distroId = $value->Id;
				$stmt->bindParam(1,$distroId,PDO::PARAM_INT);
				$stmt->bindParam(2,$id);
				$stmt->execute();
			}	
		}
		public function NewVisitor($referrer){
			$query = "Insert into Visitor (Date,Referrer) Values(CURRENT_TIMESTAMP,?)";
			$stmt = $this->db->conn->prepare($query);
			$stmt->bindParam(1,$referrer);
			$stmt->execute();
		}
		public function GetTestCount(){
			$query = "Select count(Id) as count from Result";
			$count = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS)[0];
			return $this->Output($count->count);
		}
		public function GetInstalledDistros(){
			$query = "Select Name,Homepage  from Distribution";
			$distros = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($distros);
		}
		public function GetStats(){
			$query="Select Name,Homepage, (
			 Select count(r.Id) from ResultDistro r where r.DistroId = d.Id
			) as count from Distribution d 
			order by count desc;";
			$distros = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($distros);
		}
		private function GenerateSitemapsXML(){
			header("Content-Type: text/xml");
			$xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">';
			$distros = json_decode($this->GetDistributions());
			$date = date("Y-m-d",time());
			$xml .="<url>\n<loc>".__LDC_HOME__."/</loc>\n<lastmod>".$date."</lastmod>\n<changefreq>monthly</changefreq><priority>0.9</priority></url>";
			foreach ($distros as $key => $value) {
				$xml .="<url>\n<loc>".__LDC_HOME__."/detail.php?id=".$value->Id."</loc>\n<lastmod>".$date."</lastmod>\n<changefreq>monthly</changefreq><priority>0.9</priority></url>";
			}
			$xml .="</urlset>";
			file_put_contents("sitemap.xml", $xml);
		}
	}
?>