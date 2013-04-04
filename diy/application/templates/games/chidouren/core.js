/**
 * 
 * @author Kris Cieslak
 * @version v1.0 (beta)
 * @license (Creative Commons) http://creativecommons.org/licenses/by-nc-sa/3.0/
 *
 * //digitalinsane.com
 */
var YD=YAHOO.util.Dom;
var YE=YAHOO.util.Event;
var YA=YAHOO.util.Anim;
var $ = function (el) { return YD.get(el);}
var pos = function (id,x,y) { YD.setStyle(id,"left",x+'px');YD.setStyle(id,"top",y+'px');}
var numVal = function (val) {
	  if (isNaN(val)) {
	  	  if (val.indexOf('%')!=-1) val=val.substring(0,val.indexOf('%'));
		  if (val.indexOf('px')!=-1) val=val.substring(0,val.indexOf('px'));
		  if (val.indexOf('em')!=-1) val=val.substring(0,val.indexOf('em'));
	  } else return val;
	  return parseInt(val);
  }
// -=-==--=-=-=-=-=-=--=--=-=-=-=-=-=-=-=-==-=--=-=-==--=-=-=-=-=-=-=-=-=-=-=
//   PACMAN
// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-
YAHOO.namespace('pacman');
/*  pm.gif
      frame 0 - death
      frame 1 - left run
      frame 2 - righ run
      frame 3 - left stop
      frame 4 - right stop
      frame 5 - down run
      frame 6 - up run
      frame 7 - down stop
      frame 8 - up stop
      frame 9 - clear */

// -=-=-==--=-= MAZE MATRIX 27x30
YAHOO.pacman = function () {
    var pmspeed=80;
	var gspeed=90;
	var dotscount=244;
	var score=0;
	var level=1;
	var lives=3;
	var ghostInterval;
    function ScrToMatrix(nr) { return Math.round((numVal(nr)/18)); };
	function MatrixToScr(nr) { return ((18*nr)+3) };
// Wall box position =--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
	function Walls(mx,my) {
         if ((my==2) && ( (mx>=2 && mx<=4) || (mx>=7 && mx<=10) || (mx>=16 && mx<=19) || (mx>=22 && mx<=24) )) return true;
         if ((my==3) && ( (mx>=2 && mx<=4) || (mx>=7 && mx<=10) || (mx>=16 && mx<=19) || (mx>=22 && mx<=24) )) return true;
         if ((my==6) && ( (mx>=2 && mx<=4) || (mx>=10 && mx<=16) || (mx>=22 && mx<=24) )) return true;
         if ((mx==7) && ( (my>=6 && my<=12) || (my>=15 && my<=18) || (my>=24 && my<=27) )) return true;
         if ((my==9) && ( (mx>=7 && mx<=10) || (mx>=16 && mx<=19) || (mx>=0 && mx<=4) || (mx>=22 && mx<=26) ) ) return true;
	 	 if ((mx==10) && (my==15)) return true;
	     if ((mx==4) && ( (my>=9 && my<=12) || (my>=15 && my<=18) || (my>=21 && my<=24) ) ) return true;
         if ((my==12) && ((mx>=0 && mx<=4) || (mx>=22 && mx<=26) || (mx==10 || mx==11 || mx==15 || mx==16) )) return true;
         if ((mx==13) && ((my>=0 && my<=3) || (my>=6 && my<=9) || (my>=18 && my<=21) || (my>=24 && my<=27))) return true;
         if ((my==15) &&  ((mx>=0 && mx<=4) || (mx>=22 && mx<=26) || (mx==11) || (mx==15) ))  return true;
   	     if ((mx==16) && (my==15)) return true;
         if ((my==18) &&  ((mx>=0 && mx<=4) || (mx>=22 && mx<=26) || (mx>=10 && mx<=16) ))  return true;
         if ((mx==19) && ((my>=6 && my<=12) || (my>=15 && my<=18) || (my>=24 && my<=27) )) return true;
         if ((my==21) && ((mx>=2 && mx<=4) || (mx>=7 && mx<=10) || (mx>=16 && mx<=19) || (mx>=22 && mx<=24) )) return true;
         if ((mx==22) && ((my>=9 && my<=12) || (my>=15 && my<=18) || (my>=21 && my<=24) )) return true;
         if ((my==24) &&  ((mx>=10 && mx<=16) || (mx>=0 && mx<=1) || (mx>=25 && mx<=26) ))  return true;
         if ((my==27) &&  ((mx>=2 && mx<=10) || (mx>=16 && mx<=24) ))  return true;

   	     if ((mx==-1) || (my==-1) || (mx==27) || (my==30)) return true;
		 return false;
	}
// Dots generator -==-=-=-=-=-=-=-=-=-=-=-=-==--=-=-=-=-==--==-
   function GenerateDots(){
   	for (var i = 0; i < 25; i++) {
   		Dot(106, 16 + (18 * (i+1))); Dot(376, 16 + (18 * (i+1))); Dot(16 + (18 * i),520);
     	if (i<12) {   Dot(16 + (18 * i), 16);   Dot(268 + (18 * i), 16); }
		if (i<7) {  Dot(16,34 + (18 * i));  Dot(466,34 + (18 * i));	}
		if (i<14) {  Dot(124 + (18 * i),88);}
		if (i<5) {Dot(124+ (18 * i),412);Dot(124+ (18 * i),358);Dot(286+ (18 * i),358);	Dot(286+ (18 * i),412);}
		if (i<4) {	Dot(34 + (18 * i),88);Dot(34 + (18 * i),142);Dot(394 + (18 * i),88);
					Dot(394 + (18 * i),142); Dot(16,358 + (18 * i));Dot(394 + (18 * i),358);	
 					Dot(34 + (18 * i),466);	Dot(34 + (18 * i),358);	Dot(466,466 + (18 * i));	
					Dot(394 + (18 * i),466); Dot(214,358+ (18 * i));Dot(268,358+ (18 * i));	}
		if (i<3) {	Dot(214,34 + (18 * i));	Dot(268,34 + (18 * i));	Dot(160,106 + (18 * i));
					Dot(322,106 + (18 * i));Dot(178 + (18 * i),142);Dot(268 + (18 * i),142);
					Dot(16,466 + (18 * i));	Dot(52,412 + (18 * i));	Dot(466,358 + (18 * i));				
					Dot(430 + (18 * i),412);Dot(160,430 + (18 * i));Dot(322,430 + (18 * i));							
		   		    Dot(178 + (18 * i),466);Dot(268 + (18 * i),466);}
		if (i<2) {	Dot(430,430 + (18 * i));Dot(214,484 + (18 * i));Dot(268,484 + (18 * i));}
   	} Dot(34,412);	
   BigDot('16-412');    BigDot('466-412');   BigDot('16-52');    BigDot('466-52'); 
   }
  // setClearInterval
  function ResetInterval(speed) {
        clrInt();
		clyde.interval=window.setInterval(function () {clyde.move();},speed);
		inky.interval=window.setInterval(function () {inky.move();},speed);		
		pinky.interval=window.setInterval(function () {pinky.move();},speed);				
		blinky.interval=window.setInterval(function () {blinky.move();},speed);						
  }
  // Show/Hide dot -=-=-=-=-=-=-=
  function HideDot(id) {
	 	if (YD.getStyle(id, "display") == "block") {
	 		YD.setStyle(id, "display", "none");
	 		dotscount--;
			SetScore(score+10);
			$('sc').innerHTML="Score: "+score;
			if ((id=='466-52') || (id=='466-412') || (id=='16-52') || (id=='16-412')) {
                clyde.state=blinky.state=inky.state=pinky.state=1;
			    clyde.sframe(); pinky.sframe();inky.sframe();blinky.sframe();				   				   
				ResetInterval(120);
				SetScore(score+40);
				window.setTimeout(function(){
				   clyde.state=pinky.state=inky.state=blinky.state=0;
				   clyde.sframe(clyde.direction-2);
   				   pinky.sframe(clyde.direction-2);
   				   inky.sframe(clyde.direction-2);				   
   				   blinky.sframe(clyde.direction-2);				   				   
	   			   ResetInterval(gspeed);
			},10000);
			}

	 	}
  }
 // Show/Hide all dots -=-=-=-=-=-=
  function SwitchDots(flag) {
  	 if (!flag) {	
	    YD.getElementsByClassName("small-dot","div","maze",function (el){ YD.setStyle(el.id,"display","none"); }); 	
		YD.getElementsByClassName("big-dot","div","maze",function (el){ YD.setStyle(el.id,"display","none"); }); 	
		dotscount=0;
	 } else { 
	   YD.getElementsByClassName("small-dot","div","maze",function (el){ YD.setStyle(el.id,"display","block"); }); 	
  	   YD.getElementsByClassName("big-dot","div","maze",function (el){ YD.setStyle(el.id,"display","block"); }); 	
	   dotscount=244; 
	   }
  }   
  // CreateDot -=-=-=-==-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-
   function Dot(x,y) {
   	  var e=document.createElement('div');
	  e.id=x+'-'+y;
	  $('maze').appendChild(e);
	  YD.addClass(e.id,'small-dot');
	  YD.setStyle(e.id,"left",x+"px");
  	  YD.setStyle(e.id,"top",y+"px");
   }
  //TransformSmallDot2BigDot =-=--==--==--=-=-=-=-=-=-=-=-=-=-=-==-=-=
  function BigDot(id) {
  	   if (YD.hasClass(id,'small-dot')) YD.replaceClass(id,'small-dot','big-dot');
	   YD.setStyle(id,'left',(numVal(YD.getStyle(id,'left'))-6)+'px');
	   YD.setStyle(id,'top',(numVal(YD.getStyle(id,'top'))-6)+'px');   
  }
   // SetScore -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
   function SetScore(nr) { score=nr;  $('sc').innerHTML="Score: "+score;  }
   function SetLevel(nr) { level=nr;  $('lv').innerHTML="Level: "+level;  }
   function SetLives(nr) {
   	        lives=nr;
			YD.getElementsByClassName("lives","div","leftpanel",function (el){ YD.setStyle(el.id,"background","none"); }); 
			for (var i=1;i<=lives;i++) YD.setStyle("l"+i,"background","url(img/pm.gif) -120px 0");
   }
   // newLevel -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
   function newLevel() {
   	   YAHOO.pacman.LockKey();
       clrInt();	   
	   SwitchDots(true);
	   SetLevel(level+1);
	   pm.moveTo(13,22);    	
	   clyde.sframe(6);blinky.sframe(5);inky.sframe(1);pinky.sframe(2);
	   clyde.state=0;blinky.state=0;inky.state=0;pinky.state=0;
  	   clyde.moveTo(12,13);blinky.moveTo(13,13);inky.moveTo(12,13);pinky.moveTo(13,13);			
	   pm.sframe(3);
	   window.setTimeout(function(){
	   	MoveKey(3);
	   	YE.addListener(document, 'keydown', YAHOO.pacman.UnLockKey);
		ResetInterval(gspeed);
		
	   },2000);
   }
   // death -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==--=-=-=-==--=-==-
   function death() {
      YAHOO.pacman.LockKey();
	  YE.removeListener(document,'keydown');
       clrInt();	  
	  window.clearInterval(pm.interval);
	  pm.sframe(0);
	  SetLives(lives-1);
	  window.setTimeout(function(){
	   	MoveKey(3);
 	    pm.moveTo(13,22);
		pm.sframe(3); 	        
	   	YE.addListener(document, 'keydown', YAHOO.pacman.UnLockKey);
		clyde.moveTo(12,13);blinky.moveTo(13,13);inky.moveTo(12,13);pinky.moveTo(13,13);			
		clyde.sframe(6);blinky.sframe(5);inky.sframe(1);pinky.sframe(2);
		clyde.state=0;blinky.state=0;inky.state=0;pinky.state=0;
        if (lives<0) {
			YD.setStyle('infobox','display','block');
			$('infobox').innerHTML='GAME OVER';
	        clrInt();		
			clyde.sframe(7);blinky.sframe(7);inky.sframe(7);pinky.sframe(7);
 	        YAHOO.pacman.LockKey();
			return 0;
		}
        ResetInterval(gspeed);
	   },1000);
   }
   function clrInt() {
   		    window.clearInterval(clyde.interval);
		    window.clearInterval(inky.interval);
		    window.clearInterval(pinky.interval);		
		    window.clearInterval(blinky.interval);				
   }
  // CSprite Object -==-=--==- Ghosts and Pacman =-=-=-=-==-=-
	var CSprite = function (id,x,y) {
		 this.mx = function(){	return ScrToMatrix(YD.getStyle(this.id,"left"));	 }
 		 this.my = function(){	return ScrToMatrix(YD.getStyle(this.id,"top"));	 }
		 this.ox = x;
		 this.oy = y;
		 this.id = id;
		 this.interval;
		 this.flag=false;
		 this.dx=15;
		 this.direction;
		 this.buf;
		 this.state=0;
		 this.sframe = function (frame){
		   if (this.state==0) {
  		     if (frame>=0 && frame<=4)  YD.setStyle(this.id,"background-position",(frame*-30)+"px 0"); 
  		     else YD.setStyle(this.id,"background-position",(frame*-30)+"px 30px");	
		    }
		  if (this.state==1) {
  		     if (frame>=0 && frame<=4)  YD.setStyle(this.id,"background-position","0 0"); 
  		     else YD.setStyle(this.id,"background-position","0 0");	 
		  }
		  if (this.state==2) {
  		     if (frame>=0 && frame<=4)  YD.setStyle(this.id,"background-position",(9*-30)+"px 30px"); 
  		     else YD.setStyle(this.id,"background-position",(9*-30)+"px 30px");	 
		  }
	     this.direction=frame+2;
		 }
		 this.moveTo = function (mx,my) {
           if (!Walls(mx, my) && !Walls(mx + 1, my) && !Walls(mx, my + 1) && !Walls(mx + 1, my + 1)) {
		   	pos(this.id, MatrixToScr(mx), MatrixToScr(my));
		   	this.ox = mx;
		   	this.oy = my;
		   }
		   else 
		   	if (this.id == "pacman") {
		   		window.clearInterval(this.interval);
		   		this.sframe(this.direction)
		   	}
		   	else {
               if (this.dx>0) {
 				  var x=random();
				  var z=(this.direction-2);
  				  if (z==6 || z==5) {
					  if (x==0) {if (this.choice(1)) this.sframe(1); else this.sframe(2);	}	
					  if (x==1) {if (this.choice(2)) this.sframe(2); else this.sframe(1);	}}
				  if (z==2 || z==1) {
					  if (x==0) {if (this.choice(5)) this.sframe(5); else this.sframe(6);	}
					  if (x==1) {if (this.choice(6)) this.sframe(6); else this.sframe(5);	}}
				} else 	this.direction=0;	
			}
		 } 
	}
	CSprite.prototype.choice = function(pos) {
		switch (pos){
			case 1: return !Walls(this.mx() - 1, this.my()) && !Walls(this.mx() - 1, this.my() + 1);
			case 2: return !Walls(this.mx() + 2, this.my()) && !Walls(this.mx() + 2, this.my() + 1);
			case 5: return !Walls(this.mx(), this.my() + 2) && !Walls(this.mx() + 1, this.my() + 2);
			case 6: return !Walls(this.mx(), this.my() - 1) && !Walls(this.mx() + 1, this.my() - 1);
		}
	}
	CSprite.prototype.colDet = function()  {
      if (  ((this.mx()+1>=pm.mx() && this.mx()+1<=pm.mx()+2) || ((this.mx()<=pm.mx()+1) && (this.mx()>=pm.mx()+1))) &&
		((this.my()+1>=pm.my() && this.my()+1<=pm.my()+2) || ((this.my()<=pm.my()+1) && (this.my()>=pm.my()+1)))) return true;
		return false;
	}
	function random() {	return Math.floor(Math.random()*2); }
	CSprite.prototype.move = function () {
	     if (this.id != "pacman") {
             if (this.colDet()) {
			 	if (this.state == 0) {	death();return 0}
				if (this.state == 1) { SetScore(score+200); this.state=2; this.sframe();}
			 }
			 if (this.mx() == 12 && this.my() == 13) { 	
			    this.state = 0;	this.sframe(this.direction - 2); 
				
			}
             if (this.dx>0) this.dx--; 
			 else
			 {
				this.flag=false;
			 	var xp,yp;
				if (this.state==0) {
			 	  if (this.id=='clyde') { xp = pm.mx()+1;yp = pm.my()+1;	}
				  if (this.id=='blinky') { xp = pm.mx(); yp = pm.my();}
			      if (this.id=='inky') { xp = pm.mx()+2; yp = pm.my()+2;}
			      if (this.id=='pinky') { xp = pm.mx()+3; yp = pm.my()+3;}				
                } else
				{	xp =12;yp=13;	}
				
				if (!Walls(this.mx() + 2, this.my()) && !Walls(this.mx() + 2, this.my() + 1)) 
					if (this.direction - 2 != 1) {
						if (Math.abs((this.mx() + 1) - xp) < Math.abs((this.mx() - xp))) {this.sframe(2);this.flag = true;}	}							
	   		   	if (!Walls(this.mx() - 1, this.my()) && !Walls(this.mx() - 1, this.my() + 1)) 
                        if (this.direction - 2 != 2) 
							if (Math.abs((this.mx() - 1) - xp) < Math.abs((this.mx() - xp))){this.sframe(1);this.flag = true;	}
			   	if (!Walls(this.mx(), this.my()-1) && !Walls(this.mx() +1, this.my() - 1)) 
					    if (this.direction - 2 != 5) 
							if (Math.abs((this.my() - 1) - yp) < Math.abs((this.my() - yp))) { this.sframe(6);this.flag = true;	}
     		   	if (!Walls(this.mx(), this.my()+2) && !Walls(this.mx() +1, this.my() + 2)) 
					    if (this.direction - 2 != 6) 
							if (Math.abs((this.my() + 1) - yp) < Math.abs((this.my() - yp))) {	this.sframe(5);	this.flag = true;}
  				if (!this.flag) this.dx = 15;
			 }
	   } 
		  switch (this.direction) {
		  	case 3:{ if (this.buf != this.direction) {
             	        if ((this.buf==7) && (!Walls(this.mx(),this.my()+2))) this.sframe(5);
				        if ((this.buf==8) && (!Walls(this.mx(),this.my()-1))) this.sframe(6);  	}
				if ( ((this.mx()-1)==-1) && (this.my()==13) ) { this.moveTo(25,13); break;  }
				this.moveTo(this.mx()-1,this.my()); break; 	}
		  	case 4:{ if (this.buf != this.direction) {
             	        if ((this.buf==7) && (!Walls(this.mx()+1, this.my()+2))) this.sframe(5);
             	        if ((this.buf==8) && (!Walls(this.mx()+1, this.my()-1))) this.sframe(6);  }
				if ( ((this.mx()+1)==26) && (this.my()==13) ) { this.moveTo(0,13); break;  }
				this.moveTo(this.mx()+1,this.my()); break; }
		  	case 7:{ if (this.buf != this.direction) {
					    if (this.buf == 4 && (!Walls(this.mx() + 2, this.my() +1)) && (!Walls(this.mx() + 2, this.my()+1))) this.sframe(2);
					    if (this.buf == 3 && (!Walls(this.mx() - 1, this.my() + 1)) && (!Walls(this.mx() - 1, this.my()+1))) this.sframe(1);  }
   			    this.moveTo(this.mx(),this.my()+1); break; }
		  	case 8:{ if (this.buf!=this.direction) {
                        if (this.buf==4 && (!Walls(this.mx()+ 2, this.my()-1)) && (!Walls(this.mx()+ 2, this.my()))) this.sframe(2);
                        if (this.buf==3 && (!Walls(this.mx()-1,this.my()-1)) && (!Walls(this.mx()-1,this.my()))) this.sframe(1);  }
   			    this.moveTo(this.mx(),this.my()-1); break; }
		  }
 	     if (this.id == 'pacman') {
		 	if (dotscount == 0) newLevel();
			var dotid=(numVal(YD.getStyle("pacman", "left")) + 13) + '-' + (numVal(YD.getStyle("pacman", "top")) + 13);
	 	    HideDot(dotid);
		 } 	
	}
  // Pacman control -==--=-=-=-==-=--=-=-=-=-=-=-=-=-=-==-=--=-=-=-=-==--==--==--=-==--==-=--=-=-=-==--=-=	
	function MoveKey(d) {
		function MKrestart() {
			pm.sframe(d-2);  window.clearInterval(pm.interval); pm.interval = window.setInterval(function(){pm.move()}, pmspeed);}
		pm.buf=d;
		if (pm.direction != d) 
		switch (d){
		 case 3:if ((!Walls(pm.mx() - 1, pm.my())) && (!Walls(pm.mx() - 1, pm.my() + 1))) MKrestart();break;
  		 case 4:if ((!Walls(pm.mx() + 2, pm.my())) && (!Walls(pm.mx() + 2, pm.my() + 1))) MKrestart();break;
         case 7:if ((!Walls(pm.mx(), pm.my() + 2)) && (!Walls(pm.mx() + 1, pm.my() + 2))) MKrestart();break;
		 case 8:if ((!Walls(pm.mx(), pm.my() - 1)) && (!Walls(pm.mx() + 1, pm.my() - 1))) MKrestart();break;
		}
	}
  // -=-=-=-=-==-=-=-=-=--==--=-=-=-=-=-=-=-=-=-=-=-	
   var pm = new CSprite("pacman",0,0);		
   var clyde =new CSprite("clyde",0,0);
   var blinky =new CSprite("blinky",0,0);   
   var inky =new CSprite("inky",0,0);
   var pinky =new CSprite("pinky",0,0);   
	return {
		StartGame: function () {
			SwitchDots(true);SetScore(0);SetLevel(0);SetLives(3);
 	        YE.removeListener(document,'keydown');
			YE.addListener(document,'keydown',YAHOO.pacman.UnLockKey);
			YD.setStyle('infobox','display','none');
		    pm.moveTo(13,22);MoveKey(3); 	
			clyde.moveTo(12,13);blinky.moveTo(13,13);inky.moveTo(12,13);pinky.moveTo(13,13);			
			clyde.sframe(6);blinky.sframe(5);inky.sframe(1);pinky.sframe(2);
			ResetInterval(gspeed);
		},
        UnLockKey: function (e) {
			 switch (YE.getCharCode(e)) {
              case (37): /* left */ MoveKey(3); break;
              case (39): /* right */MoveKey(4); break;
			  case (40): /* down */ MoveKey(7);  break;
			  case (38): /* up   */ MoveKey(8);  break;
            }
		},	
		MenuKey: function (e) {
			if (YE.getCharCode(e)==13) YAHOO.pacman.StartGame();
		},
		LockKey: function () {
 	        YE.removeListener(document,'keydown');
			YE.addListener(document,'keydown',YAHOO.pacman.MenuKey);
		},
		init: function () {
			 GenerateDots();
 			 clyde.moveTo(12,13);blinky.moveTo(13,13);inky.moveTo(12,13);pinky.moveTo(13,13);			
 			 YD.setStyle('infobox','display','block');
			 YE.addListener(document,'keydown',YAHOO.pacman.MenuKey);
		}
	}
} ();
function init() {
	YAHOO.pacman.init();
}
YE.addListener(window,'load',init);
