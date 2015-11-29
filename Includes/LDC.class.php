<?php
	define("__LDC_VERSION__","2.0");
	define("__LDC_HOME__","http://distrochooser.de");
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
			$useragent = $_SERVER['HTTP_USER_AGENT'];
 
			$query = "Insert into Result (Date,UserAgent) Values(CURRENT_TIMESTAMP,?)";			
			$stmt = $this->db->conn->prepare($query);
			$stmt->bindParam(1,$useragent);
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
			$useragent = $_SERVER['HTTP_USER_AGENT'];

			$query = "Insert into Visitor (Date,Referrer,UserAgent) Values(CURRENT_TIMESTAMP,?,?)";
			$stmt = $this->db->conn->prepare($query);
			$stmt->bindParam(1,$referrer);
			$stmt->bindParam(2,$useragent);
			$stmt->execute();
		}
		public function GetTestCount(){
			$query = "Select count(Id) as count from Result";
			$count = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS)[0];
			return $this->Output($count->count);
		}
		public function GetInstalledDistros(){
			$query = "Select Name,Homepage  from Distribution order by Name";
			$distros = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($distros);
		}
		public function GetStats(){
			$query="Select Name,Homepage,ColorCode, (
			 Select count(r.Id) from ResultDistro r where r.DistroId = d.Id
			) as count from Distribution d 
			order by count desc;";
			$distros = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($distros);
		}
		public function GetMonthStats(){
			//$query="SELECT COUNT( Id ) as count , MONTH( DATE ) AS 
			//MONTH FROM Result
			//WHERE YEAR( DATE ) = YEAR( CURDATE( ) ) 
			//GROUP BY MONTH desc";
			$query="SELECT COUNT( Id ) as count , DATE_FORMAT(DATE, '%d/%m') AS
			 MONTH FROM Result
			WHERE YEAR( DATE ) = YEAR( CURDATE( ) )
			and MONTH(DATE) = MONTH(CURDATE())
			GROUP BY DATE_FORMAT(DATE, '%d.%m.%Y') desc";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($result);
		}		
		public function GetTodayHits(){
			$query = "Select count(id) as Anzahl from Visitor where Date(DATE)= curdate()";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($result[0]->Anzahl);
		}
		public function GetUniqueBacklinks(){
			$query ="SELECT count(id) as Anzahl FROM `Visitor`
			where Referrer not like '%google%' and Referrer not like 'http://distrochooser.0fury.de%'and Referrer not like 'http://distrochooser2.0fury.de%' and Referrer not like
			'http://distrochooser.de%' and Referrer <> ''";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
			return $this->Output($result[0]->Anzahl);
		}
		public function GetBrowserFamilies(){
			$query = "Select count(id) as Trident,(
			     Select count(id) from Visitor where UserAgent like '%Firefox%' 
			and date(Date) = curdate()
			    ) as Gecko,(
			     Select count(id) from Visitor where UserAgent like '%Webkit%' 
			and date(Date) = curdate()
			    ) as Webkit  
			    
			    from Visitor where UserAgent like '%Trident%' 
			and date(Date) = curdate()
			";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);			
			return $this->Output($result[0]);
		}
		public function GetBotVisitorsPerDay(){
			$query = "Select count(id) as Anzahl, UserAgent from Visitor where UserAgent like '%Bot%' and Date(Date) = curdate()";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);		
			return $this->Output($result);
		}
		public function GetResultCountToday(){			
			$query = "SELECT count(id) as Anzahl FROM `Result` WHERE date(date) = curdate();";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);		
			return $this->Output($result[0]->Anzahl);
		}
		public function GetVisitorOperatingsystem(){
			$query = "call VisitorOperatingSystemsCurrentMonth();";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);		
			return $this->Output($result);
		}
		public function GetReferrerStats(){
			$query = "call RefStatsImportant();";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);		
			return $this->Output($result);
		}
		public function GetRating(){
                        $query = "call AverageRating();";
			$result = $this->db->conn->query($query)->fetchAll(PDO::FETCH_CLASS);
                        return $this->Output($result[0]->Average);
                }

		public function NewRating($rating){
			$useragent = $_SERVER['HTTP_USER_AGENT'];
			$query = "Insert into Rating (Rating,Date,UserAgent) Values(?,CURRENT_TIMESTAMP,?)";
			$stmt = $this->db->conn->prepare($query);
			$stmt->bindParam(1,$rating);
			$stmt->bindParam(2,$useragent);
			$stmt->execute();
			echo $rating;
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
