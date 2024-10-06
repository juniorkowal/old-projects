import javax.swing.*;
import java.awt.*;

abstract class PlayerState {
    public abstract void handleInput(Player player);
    public abstract void update(Player player);
    public static OnGroundState onGround = new OnGroundState();

    Rectangle hitBox = new Rectangle();
}

class Player {
    private PlayerState aState = PlayerState.onGround;
    
    private double aYVelocity;
    private double aXVelocity;
    
    private int aX = 300;
    private int aY = 350;
    
    private int aWidth = 40;
    private int aHeight = 40;
    
    public boolean keySpace;
    public boolean keyLeft;
    public boolean keyRight;
    public boolean onPlatform;
    public boolean onAnyPlatform;
    public boolean onMoving;
    public boolean onAnyMoving;

    public Image frontIm = new ImageIcon("img/Sprite/front.png").getImage();
    public Image leftIm = new ImageIcon("img/Sprite/left.png").getImage();
    public Image rightIm = new ImageIcon("img/Sprite/right.png").getImage();
    public Image jumpIm = new ImageIcon("img/Sprite/Jump.png").getImage();
    public Image jump_l_Img = new ImageIcon("img/Sprite/Jump_l.png").getImage();
    public Image jump_r_Img = new ImageIcon("img/Sprite/Jump_r.png").getImage();
    public Image Sprite = frontIm;
    public int spriteId = 1;  //Potrzebne przy nagrywaniu
    
    
    public void setState(PlayerState State){
        aState = State;
    }
    
    public void setYVelocity(double YVelocity){
        aYVelocity = YVelocity;
    }
    public double getYVelocity(){
        return aYVelocity;
    }
    public void setXVelocity(double XVelocity){
        aXVelocity = XVelocity;
    }
    public double getXVelocity(){
        return aXVelocity;
    }
    
    public int getX(){
        return aX;
    }
    public int getY(){
        return aY;
    }
    public void setX(int X){
        aX = X;
    }
    public void setY(int Y){
        aY = Y;
    }
    public int getWidth(){
        return aWidth;
    }
    public int getHeight(){
        return aHeight;
    }
    
    public void handleInput(){
       aState.handleInput(this);
    }
    
    public void update(){
      aState.update(this);
    }
}

class OnGroundState extends PlayerState{
    @Override
    public void handleInput(Player player) {

    	hitBox.x = player.getX();
    	hitBox.y = player.getY();
    	hitBox.width = player.getWidth();
    	hitBox.height = player.getHeight();
    	
    	if(player.keyLeft && player.keyRight || !player.keyLeft && !player.keyRight) {
    		if(!player.onAnyMoving)player.setXVelocity(player.getXVelocity()*0.8);
    		else player.setXVelocity(0);
    		if(player.getXVelocity() <= 0.5 && player.getXVelocity() >= -0.5) {
    		    player.Sprite = player.frontIm;
    		    player.spriteId = 1;
            }
    	} else if(player.keyLeft&&!(player.keyRight)) {
    		player.setXVelocity(player.getXVelocity()-1);
    		player.Sprite = player.leftIm;
    		player.spriteId = 2;
    	} else if(player.keyRight&&!(player.keyLeft)) {
    		player.setXVelocity(player.getXVelocity()+1);
    		player.Sprite = player.rightIm;
    		player.spriteId = 3;
    	}
    	if (player.getYVelocity() != 0) {
    	    player.Sprite = player.jumpIm;
    	    player.spriteId = 4;
        }
    	if(player.getYVelocity() != 0 && player.getXVelocity() <= -0.5) {
    	    player.Sprite = player.jump_l_Img;
    	    player.spriteId = 5;
        }
    	if(player.getYVelocity() != 0 && player.getXVelocity() >= 0.5){
    	    player.Sprite = player.jump_r_Img;
    	    player.spriteId = 6;
        }

        if(player.onAnyPlatform) player.setYVelocity(1); //Zapobiega migotaniu systemu kolizji

    	if (player.keySpace){
        	hitBox.y ++;
            for(Wall wall: World.walls) {
                if(wall.hitBox.intersects(hitBox)) {
            		player.setYVelocity(-11);
            	}
            
            }
            hitBox.y--;
        }
        
        if(!player.onAnyPlatform) player.setYVelocity(player.getYVelocity()+0.3); //Zapobiega migotaniu systemu kolizji

        //Kolizja ze sciana
        hitBox.x += player.getXVelocity();
        for(Wall wall: World.walls) {
        	if(hitBox.intersects(wall.hitBox)) {
        		hitBox.x -= player.getXVelocity();
        		while(!wall.hitBox.intersects(hitBox)) {
        			hitBox.x += Math.signum(player.getXVelocity());
        		}
        		hitBox.x -= Math.signum(player.getXVelocity());
        		player.setXVelocity(0);
        		player.setX(hitBox.x);
        	}
        }
        
        //Kolizja z ziemia
        hitBox.y += player.getYVelocity();
        for(Wall wall: World.walls) {
        	if(hitBox.intersects(wall.hitBox)) {
        	    player.onPlatform = true; // Czy player znajduje sie na platformie uzyte do anulowania podazania za ruchoma platforma
                //If zapewniajacy jednokrotne sprawdzenie czy platforma ruchoma, inaczej sprawdzalby w kazdym FPS
                if(World.licznikWys != wall.id) {
                    if(Math.random() <= World.prawdRuchomego){
                        for(Wall wallKandydat: World.walls){
                            if(wallKandydat.id == (wall.id + 3)){ wallKandydat.ruchoma = true; }
                        }
                    }
                }
        	    World.licznikWys = wall.id; //Licznik wysokosci

        	    hitBox.y -= player.getYVelocity();
        		while(!wall.hitBox.intersects(hitBox)) {
        			hitBox.y += Math.signum(player.getYVelocity());
        		}
        		hitBox.y -= Math.signum(player.getYVelocity());
        		World.cameraY+=player.getY()-hitBox.y;
        		player.setYVelocity(0);
        		hitBox.y=player.getY();
        		player.setY(hitBox.y);

        		//Gracz podaza za ruchoma platforma
                if(wall.ruchoma){
                    player.onMoving = true;
                    switch(wall.Kierunek){
                        case -1:
                            player.setXVelocity(player.getXVelocity() - 1);
                            break;
                        case 1:
                            player.setXVelocity(player.getXVelocity() + 1);
                            break;
                    }
                }
        	}

        }
        //Zapobiega migotaniu systemu kolizji i pamieta stan playera
        if(player.onPlatform) player.onAnyPlatform = true;
        else player.onAnyPlatform = false;
        if(player.onMoving) player.onAnyMoving = true;
        else player.onAnyMoving = false;
        player.onMoving = false;
        player.onPlatform = false;


        if(player.onAnyMoving){
            if(player.keyLeft && player.keyRight || !player.keyLeft && !player.keyRight) {
            } else if(player.keyLeft&&!(player.keyRight)) {
                player.setXVelocity(player.getXVelocity()-1);
            } else if(player.keyRight&&!(player.keyLeft)) {
                player.setXVelocity(player.getXVelocity()+1);
            }
        }


        
        }
    

    @Override
    public void update(Player player) {
    	
    	//Ograniczenie predkosci X
    	if(player.getXVelocity()>7) player.setXVelocity(7);
    	if(player.getXVelocity()<-7) player.setXVelocity(-7);
    	
    	player.setX(player.getX()+(int)(player.getXVelocity()));
    	
    	//Ustawianie kamery
    	World.cameraY-=(int)(player.getYVelocity());

    }
}
