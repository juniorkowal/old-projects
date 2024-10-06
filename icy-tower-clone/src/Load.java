import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Load {
    public void Odczytaj(Player mainPlayer)
    	//To samo co w save tylko do odczytywania i ustalania wartosci
    	throws IOException {

    		BufferedReader reader = new BufferedReader(new FileReader("img/save.txt"));

    		mainPlayer.setX(Integer.parseInt(reader.readLine()));
    		mainPlayer.setY(Integer.parseInt(reader.readLine()));
    		mainPlayer.setXVelocity(Integer.parseInt(reader.readLine()));
    		mainPlayer.setYVelocity(Integer.parseInt(reader.readLine()));
    		World.cameraY = Integer.parseInt(reader.readLine());
    		for (Wall wall : World.walls) {
				wall.x = Integer.parseInt(reader.readLine());
				wall.y = Integer.parseInt(reader.readLine());
				wall.startY = Integer.parseInt(reader.readLine());
				wall.ruchoma = Boolean.parseBoolean(reader.readLine());
				wall.Kierunek = Integer.parseInt(reader.readLine());
				wall.id = Integer.parseInt(reader.readLine());
				wall.hitBox.x = Integer.parseInt(reader.readLine());
				wall.hitBox.y = Integer.parseInt(reader.readLine());

			}

				reader.close();

    	}  	
    
}
