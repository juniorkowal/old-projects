import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class Save {
	
	public void zapisz(Player mainPlayer) 
			  throws IOException {
	    //Zapisywanie do pliku konkretnych wartosci playera i scian
	    BufferedWriter writer = new BufferedWriter(new FileWriter("img/save.txt"));
	    writer.write(String.valueOf(mainPlayer.getX()));
	    writer.newLine();
	    writer.write(String.valueOf(mainPlayer.getY()));
	    writer.newLine();
	    writer.write(String.valueOf((int)mainPlayer.getXVelocity()));
	    writer.newLine();
	    writer.write(String.valueOf((int)mainPlayer.getYVelocity()));
	    writer.newLine();
	    writer.write(String.valueOf(World.cameraY));
	    writer.newLine();
	    for(Wall wall: World.walls) {
	    	writer.write(String.valueOf(wall.x));
	    	writer.newLine();
	    	writer.write(String.valueOf(wall.y));
	    	writer.newLine();
	    	writer.write(String.valueOf(wall.startY));
	    	writer.newLine();
	    	writer.write(String.valueOf(wall.ruchoma));
	    	writer.newLine();
	    	writer.write(String.valueOf(wall.Kierunek));
	    	writer.newLine();
	    	writer.write(String.valueOf(wall.id));
	    	writer.newLine();
	    	writer.write(String.valueOf(wall.hitBox.x));
	    	writer.newLine();
	    	writer.write(String.valueOf(wall.hitBox.y));
	    	writer.newLine();
	    }
	    writer.close();
	}
	
	
}
