import java.awt.Graphics;
import java.awt.Image;
import java.awt.Rectangle;

import javax.swing.ImageIcon;

public class Wall {
	
	int x;
	int y;
	
	int width;
	int height;
	
	int startY;

	int id; //Numer identyfikacyjny stopnia

	boolean ruchoma = false;
	int Kierunek = -1; //Okresla kierunek ruchu 1-prawo, -1-lewo
	Rectangle hitBox;
	private Image platforma;
	
	public Wall(int x, int y, int width, int height, int id) {
		
		this.x=x;
		this.y=y;
		startY=y;
		this.width=width;
		this.height=height;

		this.id = id;
		
		hitBox = new Rectangle(x, y, width, height);
	}
	
	public void draw(Graphics g) {
		
		platforma = new ImageIcon("img/platform.png").getImage();
		g.drawImage(platforma,x,y,null);
		
	}
	
	public int ustaw(int cameraY) {
		y=startY+cameraY;
		hitBox.y=y;
		
		return y;
	}

	public void ruch(){
		switch(Kierunek){
			case -1:
				if(x <= 0) Kierunek = 1;
				else {x--; hitBox.x--; }
				break;
			case 1:
				if(x >= 530) Kierunek = -1;
				else { x++; hitBox.x++; }
				break;
		}
	}
}
