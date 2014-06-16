-- phpMyAdmin SQL Dump
-- version 4.2.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 16. Jun 2014 um 06:23
-- Server Version: 5.2.14-MariaDB-mariadb122~squeeze-log
-- PHP-Version: 5.3.28-1~dotdeb.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `scribblesql23`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Answer`
--

CREATE TABLE IF NOT EXISTS `Answer` (
`ID` int(11) NOT NULL,
  `Text` varchar(255) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=60 ;

--
-- Daten für Tabelle `Answer`
--

INSERT INTO `Answer` (`ID`, `Text`) VALUES
(36, 'Es sollte kostenlos sein.'),
(37, 'Ich lege Wert darauf, dass die verwendete Software auf freie Lizenzen, wie GPL, setzt.'),
(38, 'Ich bin auch bereit, gegebenenfalls für Support einen Betrag zu zahlen.'),
(39, 'Ich möchte das Betriebssystem wie gewohnt auf meinem PC installieren und dann davon starten.'),
(40, 'Ich möchte das Betriebssystem auf einem USB - Stick installieren, um es von unterschiedlichen PC''s aus zu starten'),
(41, 'Ich möchte das System nur über eine CD/ DVD starten, um z. B. mein System zu reparieren oder Viren zu entfernen.'),
(42, 'Mein PC ist noch durchaus aktuell.'),
(43, 'Etwas älter'),
(44, 'Ich habe bereits Probleme, aktuelle Software auf dem System zu nutzen.'),
(45, 'Ich bevorzuge eine grafische Benutzeroberfläche zur Verwaltung der Programme.'),
(46, 'Ich bevorzuge das aus Debian bekannte Aptitude/ APT'),
(47, 'Ich bevorzuge den aus Arch bekannten Pacman.'),
(48, 'Ich bevorzuge das aus Fedora bekannte RPM - System'),
(49, 'Ich habe von Linux keine Ahnung.'),
(50, 'Ich habe schon mal Linux verwendet.'),
(51, 'Ich benutze Linux schon länger.'),
(52, './configure && make && sudo make install'),
(53, 'Ich möchte alles aus Quelltexten bauen'),
(54, 'Die Distribution sollte eine Standardoberfläche mitbringen.'),
(55, 'Ich bevorzuge es, die Oberfläche selbst zu wählen bzw. zu installieren.'),
(56, 'Es soll nur ein Minimalumfang installiert werden. Alles andere installiere ich selbst.'),
(57, 'Nein, ich möchte nach der Installation direkt mit dem System arbeiten.'),
(58, 'Ja.'),
(59, 'Nein.');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `AnswerDistributionRelation`
--

CREATE TABLE IF NOT EXISTS `AnswerDistributionRelation` (
`ID` int(11) NOT NULL,
  `AID` int(11) NOT NULL,
  `DID` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=149 ;

--
-- Daten für Tabelle `AnswerDistributionRelation`
--

INSERT INTO `AnswerDistributionRelation` (`ID`, `AID`, `DID`) VALUES
(1, 36, 1),
(2, 36, 2),
(3, 36, 3),
(4, 36, 4),
(5, 36, 5),
(7, 36, 6),
(8, 36, 7),
(9, 36, 8),
(10, 36, 9),
(11, 36, 10),
(12, 36, 11),
(13, 36, 12),
(14, 36, 13),
(15, 37, 7),
(16, 37, 11),
(17, 38, 8),
(18, 39, 1),
(19, 39, 2),
(20, 39, 3),
(21, 39, 4),
(22, 39, 5),
(23, 39, 6),
(24, 39, 7),
(25, 39, 8),
(26, 39, 9),
(27, 39, 10),
(28, 39, 11),
(29, 40, 12),
(30, 40, 13),
(31, 41, 12),
(32, 41, 13),
(33, 44, 12),
(34, 44, 13),
(35, 43, 1),
(36, 43, 3),
(37, 43, 11),
(38, 42, 2),
(39, 42, 4),
(40, 42, 5),
(41, 42, 6),
(42, 42, 7),
(43, 42, 8),
(44, 42, 9),
(45, 42, 10),
(46, 42, 12),
(47, 42, 13),
(48, 45, 2),
(49, 45, 3),
(50, 45, 4),
(51, 45, 5),
(52, 45, 6),
(53, 45, 7),
(54, 45, 8),
(55, 45, 9),
(56, 45, 10),
(57, 45, 11),
(58, 45, 12),
(59, 45, 13),
(60, 47, 1),
(61, 47, 3),
(62, 46, 2),
(63, 46, 4),
(64, 46, 5),
(65, 46, 6),
(66, 46, 9),
(67, 46, 13),
(68, 48, 6),
(69, 48, 7),
(70, 49, 2),
(71, 49, 3),
(72, 49, 4),
(73, 49, 9),
(74, 49, 10),
(75, 50, 5),
(76, 50, 6),
(77, 50, 7),
(78, 50, 8),
(79, 50, 12),
(80, 50, 13),
(81, 51, 11),
(82, 51, 1),
(104, 36, 14),
(105, 37, 14),
(106, 39, 14),
(107, 42, 14),
(108, 43, 14),
(109, 44, 14),
(110, 53, 14),
(111, 52, 14),
(112, 55, 1),
(113, 55, 14),
(114, 54, 2),
(115, 54, 3),
(116, 54, 4),
(117, 54, 5),
(118, 54, 6),
(119, 54, 7),
(120, 54, 8),
(121, 54, 9),
(122, 54, 10),
(123, 54, 11),
(124, 54, 12),
(125, 54, 13),
(126, 56, 1),
(127, 56, 14),
(128, 57, 2),
(129, 57, 3),
(130, 57, 4),
(131, 57, 5),
(132, 57, 6),
(133, 57, 7),
(134, 57, 8),
(135, 57, 9),
(136, 57, 10),
(137, 57, 11),
(138, 57, 12),
(139, 57, 13),
(140, 58, 8),
(141, 43, 15),
(142, 47, 15),
(143, 36, 15),
(144, 45, 15),
(145, 39, 15),
(146, 49, 15),
(147, 57, 15),
(148, 54, 15);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Distribution`
--

CREATE TABLE IF NOT EXISTS `Distribution` (
`ID` int(11) NOT NULL,
  `Name` varchar(255) COLLATE utf8_bin NOT NULL,
  `Manufacturer` varchar(255) COLLATE utf8_bin NOT NULL,
  `ImageLink` varchar(255) COLLATE utf8_bin NOT NULL,
  `Description` text COLLATE utf8_bin NOT NULL,
  `License` text COLLATE utf8_bin NOT NULL,
  `Website` text COLLATE utf8_bin NOT NULL,
  `ImageSource` text COLLATE utf8_bin NOT NULL,
  `TextSource` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=16 ;

--
-- Daten für Tabelle `Distribution`
--

INSERT INTO `Distribution` (`ID`, `Name`, `Manufacturer`, `ImageLink`, `Description`, `License`, `Website`, `ImageSource`, `TextSource`) VALUES
(1, 'Arch Linux', 'Aaron Griffin', './img/linux/arch.png', 'Arch Linux ist eine i686- und AMD64-optimierte Linux-Distribution nach dem KISS-Prinzip. Aufgrund dieses minimalistischen Ansatzes ist Arch Linux als Distribution für fortgeschrittene Benutzer zu sehen, da auf grafische Installations- und Konfigurationshilfen zu Gunsten der Einfachheit verzichtet wird.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://archlinux.org', 'https://www.archlinux.org/art/', 'Zitat https://de.wikipedia.org/wiki/Arch_Linux'),
(2, 'Ubuntu', 'Canonical Ltd.', './img/linux/ubuntu.png', 'Die Entwickler verfolgen mit Ubuntu das Ziel, ein einfach zu installierendes und leicht zu bedienendes Betriebssystem mit aufeinander abgestimmter Software zu schaffen. Dies soll unter anderem dadurch erreicht werden, dass für jede Aufgabe genau ein Programm zur Verfügung gestellt wird. Das Projekt wird vom Software-Hersteller Canonical Ltd. gesponsert, das vom südafrikanischen Unternehmer Mark Shuttleworth gegründet wurde', '<a href="http://de.wikipedia.org//wiki/Open_Source" title="Open Source">Open Source</a> (u.&nbsp;a. <a href="http://de.wikipedia.org//wiki/GNU_General_Public_License" title="GNU General Public License">GNU GPL</a>)', 'http://www.ubuntu.com/', 'http://design.ubuntu.com/downloads?metadata=element-logo+brand-ubuntu', 'Zitat https://de.wikipedia.org/wiki/Ubuntu'),
(3, 'Manjaro', 'Roland Singer, Guillaume Benoit, Philip Müller u. a.', './img/linux/manjaro.png', 'Manjaro ist eine auf Arch Linux basierende Linux-Distribution, die in Deutschland, Frankreich und Österreich entwickelt wird. Es ist in erster Linie ein freies Betriebssystem für Personal Computer welches auf Benutzerfreundlichkeit ausgerichtet ist. \r\nWie seine Basis, Arch Linux, nutzt es ein Rolling-Release-Modell.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'https://wiki.manjaro.org/index.php?title=Main_Page', 'https://commons.wikimedia.org/wiki/File:Manjaro_logo_and_name_white_background.png', 'Zitat https://de.wikipedia.org/wiki/Manjaro'),
(4, 'Linux Mint', 'Linux Mint, Community', './img/linux/mint.png', 'Linux Mint ist eine Linux-Distribution, die es in zwei Varianten gibt. Die erste Variante, die Haupt-Ausgabe, basiert auf der Distribution Ubuntu. Die zweite Variante, Linux Mint Debian Edition (LMDE) genannt, beruht auf Debian testing. \r\n</br>\r\nLinux Mint enthält im Gegensatz zu Ubuntu in der Standard-Ausgabe bereits Codecs für verschlüsselte DVDs, MP3 oder DivX sowie Plugins wie Adobe Flash und Oracle Java. Zudem ist NDISwrapper für die Unterstützung von WLAN-Karten ohne eigenen Linux-Treiber vorinstalliert und es gibt einige Programme und Anleitungen, um die Kommunikation mit Windows-Systemen auf dem gleichen oder anderen Computern zu vereinfachen. Technisch benutzt man die Paketquellen von Ubuntu sowie eine weitere, eigene mit den veränderten und zusätzlichen Paketen. Dadurch sind für die Benutzer von Linux Mint alle Aktualisierungen von Ubuntu ebenfalls verfügbar.', '<a href="/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> u.&nbsp;a.; beinhaltet proprietäre Software', 'http://www.linuxmint.com/', 'https://commons.wikimedia.org/wiki/File:Linux_Mint_logo_and_wordmark.svg', 'Zitat https://de.wikipedia.org/wiki/Linux_Mint'),
(5, 'Debian', 'Das Debian-Projekt', './img/linux/debian.png', 'Debian ist ein seit 1993 gemeinschaftlich entwickeltes, freies Betriebssystem. Debian GNU/Linux, das auf den grundlegenden Systemwerkzeugen des GNU-Projektes sowie dem Linux-Kernel basiert, ist eine der ältesten, einflussreichsten und am weitesten verbreiteten GNU/Linux-Distributionen. Das heute bekannteste Debian-GNU/Linux-Derivat ist Ubuntu.', '<a href="/wiki/Debian_Free_Software_Guidelines" title="Debian Free Software Guidelines">DFSG</a>-konforme Lizenzen', 'http://www.debian.org/', 'https://commons.wikimedia.org/wiki/File:Debian-OpenLogo.svg', 'Zitat https://de.wikipedia.org/wiki/Debian'),
(6, 'Mageia', 'Mageia-Community', './img/linux/mageia.png', 'Mageia ist eine Linux-Distribution, die im September 2010 als Abspaltung von Mandriva Linux ins Leben gerufen wurde. \r\n\r\nDie Systemkonfiguration wird bei Mageia Linux mit eigenen Werkzeugen im Rahmen der „Drak-Tools“ konfiguriert – hierzu steht eine zentrale grafische Oberfläche (genannt „Mageia-Kontrollzentrum“) zur Verfügung.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://mageia.org/de/', 'https://commons.wikimedia.org/wiki/File:Mageia_Logo.png', 'Zitat https://de.wikipedia.org/wiki/Mageia'),
(7, 'Fedora', 'Fedora-Projekt', './img/linux/fedora.png', 'Fedora ist eine RPM-basierte Linux-Distribution. Ziel der Entwickler der Distribution ist es, freie Software zu fördern und ein Betriebssystem für eine möglichst vielfältige Zielgruppe zu gestalten. Organisiert wird die Entwicklung in der Online-Community des Fedora-Projekts, das vom Unternehmen Red Hat angeführt wird. Fedora ist der direkte Nachfolger von Red Hat Linux. Das englische Wort Fedora bezeichnet eine spezielle Art des Filzhuts, das Markenzeichen des Unternehmens Red Hat.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://fedoraproject.org/de/', 'https://commons.wikimedia.org/wiki/File:Fedora_logo_and_wordmark.svg', 'Zitat https://de.wikipedia.org/wiki/Fedora_(Linux-Distribution)'),
(8, 'openSuse', 'SUSE Linux GmbH und Entwickler-Community', './img/linux/opensuse.png', 'openSUSE, ehemals SUSE Linux und SuSE Linux Professional, ist eine Linux-Distribution des Unternehmens SUSE Linux GmbH. Sie wird insbesondere in Deutschland verbreitet eingesetzt. Der Fokus der Entwickler liegt darauf, ein stabiles und benutzerfreundliches Betriebssystem mit großer Zielgruppe für Desktop und Server zu erschaffen.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://www.opensuse.org/de/', 'https://commons.wikimedia.org/wiki/File:OpenSUSE_Logo.svg', 'Zitat https://de.wikipedia.org/wiki/Opensuse'),
(9, 'elementary OS', 'Daniel Fore (DanRabbit) und andere', './img/linux/elementary.png', 'elementary ist ein im Jahr 2007 entstandenes freies Software-Projekt, das ursprünglich eine Sammlung von Programmen und Designs für Ubuntu zusammenstellte, welche sich stark am „Look and Feel“ von Mac OS X orientierten. Seit März 2011 gibt es eine eigene Ubuntu-basierende Linux-Distribution unter dem Namen elementary OS. Als elementary OS Luna wurde die aktuelle Version am 11. August 2013 veröffentlicht.', '<a href="/wiki/GNU_General_Public_License" title="GNU General Public License">GNU GPL v2</a>', 'http://www.elementaryos.org/', 'https://commons.wikimedia.org/wiki/File:Elementary_logo.svg', 'Zitat https://de.wikipedia.org/wiki/Elementary_OS'),
(10, 'PCLinuxOS', 'Bill Reynolds (Texstar)', './img/linux/pclinuxos.png', 'Laut verschiedener Tests zeichnet sich PCLinuxOS durch seine Einfachheit und Benutzerfreundlichkeit sowie die überdurchschnittlich gute Hardwareerkennung aus. Von Heimanwendern oft benutzte Software wie Codecs für Multimediadateien, Flash und Java ist bei PCLinuxOS vorinstalliert, und als Standard-Arbeitsumgebung kommt KDE Plasma Desktop mit dem von Debian stammenden Paketverwaltungs-Tool APT in der Variante APT-RPM und dessen grafischem Aufsatz Synaptic zum Einsatz.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://www.pclinuxos.com/', 'https://commons.wikimedia.org/wiki/File:PCLinuxOS_logo.svg', 'Zitat https://de.wikipedia.org/wiki/PCLinuxOS#'),
(11, 'CentOS', 'CentOS-Projekt', './img/linux/centos.png', 'CentOS (Community ENTerprise Operating System) ist eine Linux-Distribution, die auf der Distribution Red Hat Enterprise Linux (RHEL) des Unternehmens Red Hat aufbaut. Die Distribution wird von einer offenen Gruppe von freiwilligen Entwicklern betreut, gepflegt und weiterentwickelt.\r\n\r\nCentOS ist hinter Debian und Ubuntu die dritthäufigste verwendete Linux-Distribution für Web-Server.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://www.centos.org/', 'http://mirror.centos.org/centos/graphics/centos-transparent.png', 'Zitat https://de.wikipedia.org/wiki/Centos'),
(12, 'Puppy Linux', 'Barry Kauler und Puppy Linux Community', './img/linux/puppy.png', 'Puppy Linux ist eine platzsparende und schnelle Linux-Distribution, die unter anderem direkt von einer Live-CD betrieben werden kann. Aus Quelltext kompiliert, basiert Puppy auf keiner anderen Linux-Distribution.\r\nDer Name leitet sich von dem inzwischen verschwundenen Chihuahua Puppy (dt.: Welpe) des australischen Projektgründers Barry Kauler ab.\r\n\r\nEin Ziel des Betriebssystems ist es, auch von Benutzern ohne Linuxkenntnisse sofort genutzt werden zu können. Die Entwickler versuchen dies durch unkomplizierte, benutzerfreundliche Bedienung und breite Hardwareunterstützung zu erreichen.', '<a href="/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> / <a href="/wiki/GNU_Lesser_General_Public_License" title="GNU Lesser General Public License">LGPL</a> (<a href="/wiki/Freie_Software" title="Freie Software">Freie Software</a>) und weitere', 'http://www.puppylinux.org/', 'https://en.wikipedia.org/wiki/File:Banner_logo_Puppy.png', 'Zitat https://de.wikipedia.org/wiki/Puppy_Linux'),
(13, 'Knoppix', 'Klaus Knopper', './img/linux/knoppix.png', 'Knoppix ist eine freie GNU/Linux-Distribution, deren Fokus auf dem Live-Betrieb liegt. Sie wird von Klaus Knopper entwickelt, von dessen Namen sich die Benennung Knoppix ableitet. Knoppix liegt hin und wieder Computerzeitschriften bei und basiert auf einer Mischung aus Debian unstable und testing. Sie wurde vom deutschen Bundesamt für Sicherheit in der Informationstechnik unterstützt und verteilt.', '<a href="/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a>', 'http://www.knopper.net/knoppix/', 'https://commons.wikimedia.org/wiki/File:Knoppix_logo.svg', 'Zitat https://de.wikipedia.org/wiki/Knoppix'),
(14, 'Gentoo Linux', 'Gentoo Foundation Inc.', './img/linux/gentoo.png', 'Gentoo Linux ist eine quellbasierte Linux-Distribution für fortgeschrittene Linux-Benutzer, die ihr System komplett individuell einrichten möchten. Voraussetzung dafür ist die Bereitschaft, sich mit den Abläufen eines Linux-Systems und der ausführlichen Dokumentation auseinanderzusetzen. Gentoo ist ein Warenzeichen der Gentoo Foundation, Inc., einer Non-Profit-Organisation.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://www.gentoo.org/', 'http://www.gentoo.org/main/en/name-logo.xml', 'https://de.wikipedia.org/wiki/Gentoo_Linux'),
(15, 'Antergos', 'Alexandre Filgueira und Weitere', './img/linux/antergos.png', 'Antergos (ehemals Cinnarch) ist eine Linux-Distribution aus Galicien, die auf dem Betriebssystem Arch Linux basiert. Es wird die Arbeitsumgebung Gnome als Standard eingerichtet, aber es kann auch mit Cinnamon, MATE, Openbox oder Xfce installiert werden.', '<a href="http://de.wikipedia.org/wiki/GNU_General_Public_License" title="GNU General Public License">GPL</a> und andere Lizenzen', 'http://www.antergos.com/', 'https://en.wikipedia.org/wiki/File:Antergos_logo_github.png', 'https://de.wikipedia.org/wiki/Antergos');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Question`
--

CREATE TABLE IF NOT EXISTS `Question` (
`ID` int(11) NOT NULL,
  `Title` text COLLATE utf8_bin NOT NULL,
  `Subtitle` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=12 ;

--
-- Daten für Tabelle `Question`
--

INSERT INTO `Question` (`ID`, `Title`, `Subtitle`) VALUES
(4, 'Lizenzmodelle: Welche Lizenz bevorzugst Du bei der Wahl eines Betriebssystems?', 'Oft wird bei Linux von "quelloffener" oder "freier" Software gesprochen. Dabei handelt es sich um Software, deren Quelltext frei, ohne Restriktionen eingesehen und verändert werden darf. </br>Eine Distribution stellt dabei kein einzelnes Produkt, sondern ein "Bündel" verschiedener Programme dar. Z. B. besteht eine klassische Distribution stark vereinfacht aus dem Linux-Kernel und einer Oberfläche.</br>Viele Distributionen bieten Support über ihre Communities an. So findet man häufig dort Antworten auf die meisten Probleme. Es gibt aber auch manche Distributionen, die auch hierzu kostenpflichtigen Support anbieten. Dieser Support ist häufig für den professionellen Einsatz, z. B. im Betrieb, gedacht.'),
(5, 'Installation: Wie möchte ich Linux auf meinem PC installieren?', 'Eine Distribution wird häufig klassisch auf der Festplatte des Computers installiert. Es ist aber auch möglich, Linux von einem USB-Stick zu nutzen. Es gibt Distributionen, die genau für diesen Betrieb geeignet sind, z. B. durch niedrigen Ressourcenverbrauch. </br></br>Bei Linux wird man auch auf den Begriff "Live Modus" stoßen. Der "Live Modus" dient dazu, ein Betriebssystem zuerst von inem Datenträger (CD/DVD, USB-Stick) zu testen, bevor man es auf dem Computer installiert. Viele Distributionen verfügen über diesen Live-Modus, der auch oft zur Datenrettung eingesetzt wird.'),
(6, 'Hardware: Mein PC ist...?', 'Die PC-Technik verändert sich von Tag zu Tag. So müssen auch die Linux-Entwickler sich an diese Gegebenheiten anpassen. So ist es unausweichlich, dass die Unterstützung für alte Hardware entfernt wird, sonst würde die Linux-Basis immer klobiger werden und schließlich könnte man den Code kaum noch warten. </br>Da Linux jedoch eine freie Software ist, entwickeln Menschen so genannte <i>Forks</i>. Ein Fork ist ein Zweig einer Software, der von der Hauptentwicklung abweicht. In diesen Forks sind dann z. B. die Unterstützung für alte Hardware noch enthalten und diese finden dann Einsatz in speziellen Distributionen, die für ältere Hardware gedacht sind.'),
(7, 'Softwaremanagement: Wie möchte ich neue Programme installieren, verwalten und ggf. entfernen?', 'Unter Linux ist es möglich, Programme auf unterschiedliche Arten zu installieren. Zunächst kann man sich diese aus dem Programmquelltext selbst "übersetzen", sodass man das Programm ausführen kann. Diese Methode richtet sich aber zunächst an erfahrene Benutzer.</br>Nahezu jede Distribution ist mit einem so genannten Paketmanagement ausgestattet. Durch dieses ist es Möglich, Programme in Form so genannter Pakete zu installieren. Beispielsweise gibt es so für den Browser "Firefox" das Paket "firefox".</br>Es existieren unterschiedliche Ansätze für Paketmanagments, bekannte Vertreter sind "apt" bei Debian/ Ubuntu, "yum" bei Fedora oder "pacman" bei Arch/ Manjaro bzw. "zypper" bei openSuse. Häufig ist es möglich, die Paketverwaltung über ein grafisches Programm durchzuführen, um die Verwendung Einsteigerfreundlich gestalten zu können.'),
(8, 'Ich beschreibe meine Linux-Kenntnisse wie folgt:', 'Linux-Distributionen unterscheiden sich teils massiv in ihren Anforderungen an die Kenntnisse der Benutzer.'),
(9, 'Betriebssystemoberfläche: Wie soll die Oberfläche auf dem System installiert werden?', 'Linux Distributionen können mit verschiedenen Oberflächen betrieben werden. Oft werden Oberflächen mit der Distribution mitgeliefert, bei anderen Distributionen wird diese per Hand installiert.'),
(10, 'Installationsumfang: Soll nur ein Minimalumfang installiert werden oder soll das System direkt nach der Installation samt aller Programme direkt einsatzbereit sein?', 'Viele Linux - Distributionen umfassen alle notwendigen Programme, ob direkt nach der Installation damit arbeiten zu können.Andere beschränken den Umfang auf ein Minimum, um dem Benutzer die freie Wahl zu lassen. Letzteres benötigt jedoch mehr Zeit.'),
(11, 'Systemverwaltung: Ich setze viel Wert darauf, bei der Administration meines Systems ein zentrales Programm zu verwenden.', 'Manche Distributionen bieten zentrale Verwaltungstools an, mit denen das System verwaltet wird.');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `QuestionAnswerRelation`
--

CREATE TABLE IF NOT EXISTS `QuestionAnswerRelation` (
`ID` int(11) NOT NULL,
  `QID` int(11) NOT NULL,
  `AID` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=29 ;

--
-- Daten für Tabelle `QuestionAnswerRelation`
--

INSERT INTO `QuestionAnswerRelation` (`ID`, `QID`, `AID`) VALUES
(1, 4, 36),
(2, 4, 37),
(4, 4, 38),
(5, 5, 39),
(6, 5, 40),
(9, 5, 41),
(10, 6, 42),
(11, 6, 43),
(12, 6, 44),
(13, 7, 45),
(14, 7, 46),
(16, 7, 47),
(17, 7, 48),
(18, 8, 49),
(19, 8, 50),
(20, 8, 51),
(21, 8, 52),
(22, 7, 53),
(23, 9, 54),
(24, 9, 55),
(25, 10, 56),
(26, 10, 57),
(27, 11, 58),
(28, 11, 59);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Stats`
--

CREATE TABLE IF NOT EXISTS `Stats` (
  `TestsMade` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Daten für Tabelle `Stats`
--

INSERT INTO `Stats` (`TestsMade`) VALUES
(743);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Answer`
--
ALTER TABLE `Answer`
 ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `AnswerDistributionRelation`
--
ALTER TABLE `AnswerDistributionRelation`
 ADD PRIMARY KEY (`ID`), ADD KEY `AID` (`AID`), ADD KEY `DID` (`DID`);

--
-- Indexes for table `Distribution`
--
ALTER TABLE `Distribution`
 ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Question`
--
ALTER TABLE `Question`
 ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `QuestionAnswerRelation`
--
ALTER TABLE `QuestionAnswerRelation`
 ADD PRIMARY KEY (`ID`), ADD KEY `AID` (`AID`), ADD KEY `QID` (`QID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Answer`
--
ALTER TABLE `Answer`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=60;
--
-- AUTO_INCREMENT for table `AnswerDistributionRelation`
--
ALTER TABLE `AnswerDistributionRelation`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=149;
--
-- AUTO_INCREMENT for table `Distribution`
--
ALTER TABLE `Distribution`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `Question`
--
ALTER TABLE `Question`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `QuestionAnswerRelation`
--
ALTER TABLE `QuestionAnswerRelation`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=29;
--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `AnswerDistributionRelation`
--
ALTER TABLE `AnswerDistributionRelation`
ADD CONSTRAINT `AnswerDistributionRelation_ibfk_1` FOREIGN KEY (`AID`) REFERENCES `Answer` (`ID`),
ADD CONSTRAINT `AnswerDistributionRelation_ibfk_2` FOREIGN KEY (`DID`) REFERENCES `Distribution` (`ID`),
ADD CONSTRAINT `FK_Answer` FOREIGN KEY (`AID`) REFERENCES `Answer` (`ID`);

--
-- Constraints der Tabelle `QuestionAnswerRelation`
--
ALTER TABLE `QuestionAnswerRelation`
ADD CONSTRAINT `QuestionAnswerRelation_ibfk_1` FOREIGN KEY (`AID`) REFERENCES `Answer` (`ID`),
ADD CONSTRAINT `QuestionAnswerRelation_ibfk_2` FOREIGN KEY (`QID`) REFERENCES `Question` (`ID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
