import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.image.BufferStrategy;
import java.io.*;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import static javax.swing.WindowConstants.EXIT_ON_CLOSE;

public class World {

    public Frame game;

    private static boolean activeLoop = true;
    private static Player mainPlayer = new Player();
    private static Sound muzyka = new Sound();
    private static Save save = new Save();
    private static Load load = new Load();
    
    private Image tlo;
    private Image platforma;
    private static boolean zatrzaskSpacja;
    
    static ArrayList<Wall> walls = new ArrayList<>();
    static int cameraY = 0;
    static int licznikWys = 0;
    static double prawdRuchomego = 0;

    private static boolean record = false;
    private static  boolean play = false;
    private static DataOutputStream RecordStream;
    private static DataInputStream PlayStream;

    public World(BufferStrategy bufStrategy){
    	muzyka.wybierzPlik("img/muzyka.wav");
    	muzyka.zapetl();
        try{
            makeWalls();
            czcionka();

            //Petla Gry;
            while(activeLoop){
                long startTime = System.currentTimeMillis();  //Do ustalenia FPS

                Graphics g = bufStrategy.getDrawGraphics();
                if(!play) {
                    processInput();
                    update();

                    //Renderowanie
                    render(g);
                    if (!bufStrategy.contentsLost()) {
                        bufStrategy.show();
                        g.dispose();
                    }
                }
                else{
                    playRecord(g);
                    if (!bufStrategy.contentsLost()) {
                        bufStrategy.show();
                        g.dispose();
                    }
                }

                Thread.yield();
                TimeUnit.MILLISECONDS.sleep(startTime + 16 - System.currentTimeMillis());
            }
            System.exit(0);

        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public static void main(String[] args){
        JFrame game = new JFrame();
        game.setIgnoreRepaint(true);
        game.setDefaultCloseOperation(EXIT_ON_CLOSE);
        game.setResizable(false);

        game.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if(e.getKeyCode() == KeyEvent.VK_ESCAPE) activeLoop = false;
                if(e.getKeyCode() == KeyEvent.VK_SPACE&&!zatrzaskSpacja) {
                    mainPlayer.keySpace = true;
                    muzyka.wybierzPlik("img/skok.wav");
                    muzyka.graj();
                    zatrzaskSpacja=true;
                }
                if(e.getKeyCode() == KeyEvent.VK_LEFT) mainPlayer.keyLeft = true;
                if(e.getKeyCode() == KeyEvent.VK_RIGHT) mainPlayer.keyRight = true;
                if(e.getKeyCode() == KeyEvent.VK_N) muzyka.wyciszMuzyke();
                if(e.getKeyCode() == KeyEvent.VK_M) muzyka.podglosnijMuzyke();
                if(e.getKeyCode() == KeyEvent.VK_S)
                    try {
                        save.zapisz(mainPlayer);
                    } catch (IOException e1) {
                        e1.printStackTrace();
                    }
                if(e.getKeyCode() == KeyEvent.VK_L)
                    try{
                        load.Odczytaj(mainPlayer);
                    }catch (IOException e1) {
                        e1.printStackTrace();
                    }
                if(e.getKeyCode() == KeyEvent.VK_R){
                    record = true;
                    try{
                        RecordStream = new DataOutputStream(new FileOutputStream("record.dat"));
                    }catch (FileNotFoundException exception) {
                        exception.printStackTrace();
                    }
                }
                if(e.getKeyCode() == KeyEvent.VK_P){
                    record = false;
                    if (play == true) play = false;
                    else {
                        play = true;
                        try {
                            PlayStream = new DataInputStream(new FileInputStream("record.dat"));
                        } catch (FileNotFoundException exception1) {
                            exception1.printStackTrace();
                        }
                    }
                }
            }
            public void keyReleased(KeyEvent e) {
                if(e.getKeyCode() == KeyEvent.VK_SPACE) mainPlayer.keySpace = false; zatrzaskSpacja=false;
                if(e.getKeyCode() == KeyEvent.VK_LEFT) mainPlayer.keyLeft = false;
                if(e.getKeyCode() == KeyEvent.VK_RIGHT) mainPlayer.keyRight = false;
                if(e.getKeyCode() == KeyEvent.VK_N) ;
                if(e.getKeyCode() == KeyEvent.VK_M) ;
                if(e.getKeyCode() == KeyEvent.VK_S) ;
                if(e.getKeyCode() == KeyEvent.VK_L) ;
            }
        });

        Canvas canvas = new Canvas();
        canvas.setIgnoreRepaint(true);
        canvas.setSize(640, 480);

        game.add(canvas);
        game.setSize(640, 510);
        game.setVisible(true);

        canvas.createBufferStrategy(2);
        BufferStrategy bufStrategy = canvas.getBufferStrategy();

        GraphicsEnvironment GraphEnv = GraphicsEnvironment.getLocalGraphicsEnvironment();
        GraphicsDevice GraphDev = GraphEnv.getDefaultScreenDevice();
        GraphicsConfiguration GraphConf = GraphDev.getDefaultConfiguration();

        new World(bufStrategy);

    }

    public void makeWalls() {
        
        walls.add(new Wall(265, 600, 90, 20, 1));
    	for(int i=0; i<600; i+=150) {
    		int losowa_pozycja = (int)Math.floor(Math.random()*(431)+70);
    		walls.add(new Wall(losowa_pozycja, i, 90, 20, 5 - i/150));
    	}
    	
    }
    
    //Ladowanie czcionki z pliku
    public void czcionka() {
    	try {
    	     GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
    	     ge.registerFont(Font.createFont(Font.TRUETYPE_FONT, new File("img/slkscre.ttf")));
    	} catch (IOException|FontFormatException e) {
    		e.printStackTrace();
    	}

    }

    public void reset() {
    	mainPlayer.setX(300);
    	mainPlayer.setY(350);
    	mainPlayer.setXVelocity(0);
    	mainPlayer.setYVelocity(0);
    	walls.clear();
    	cameraY=0;
    	makeWalls();
    	muzyka.wybierzPlik("img/przegrana.wav");
    	muzyka.graj();
    }
    
    public void render(Graphics g){
    	
        tlo = new ImageIcon("img/tlo.gif").getImage();
        
        //Rysowanie tla z efektem paralaksy
        int tloY = cameraY/2;

        while (tloY > 0) {
        	tloY -= tlo.getHeight(null);
            g.drawImage(tlo, 0, tloY, null);
        }
        
        while (tloY < tlo.getHeight(null)) {
            g.drawImage(tlo, 0, tloY, null);
            tloY += tlo.getHeight(null);
        }
        
        g.setColor(Color.BLUE);
        
        g.drawImage(mainPlayer.Sprite, mainPlayer.getX(), mainPlayer.getY(), null);

        int losowa_pozycja = (int)Math.floor(Math.random()*(431)+70);
        
        for(Wall wall: walls) {
        	wall.draw(g);
        	wall.ustaw(cameraY);
        	if(wall.y>650) {
        		wall.startY-=740;
        		wall.x=losowa_pozycja;
        		wall.hitBox.x=losowa_pozycja;
        		wall.hitBox.y=0;
        		wall.id += 5;
        		wall.ruchoma=false;
        	}
        	
        }
        
        //Skoro nie robimy scian bocznych
        if(mainPlayer.getX()>640) {
        	mainPlayer.setX(0);
        }
        if(mainPlayer.getX()<0) {
        	mainPlayer.setX(640);
        }

        if(mainPlayer.getYVelocity()>15) {
        	reset();
        }
        
        g.setFont(new Font("Silkscreen Expanded",Font.TRUETYPE_FONT,30));
        g.setColor(Color.DARK_GRAY);
        g.drawString("Wysokosc:" + licznikWys, 10, 30);
        g.setFont(new Font("Silkscreen Expanded",Font.TRUETYPE_FONT,25));
        g.drawString("Wyjscie: esc", 10, 410);
        g.drawString("Muzyka: N/M", 10, 430);
        g.drawString("Zapis/Odczyt: S/L", 10, 450);
        g.drawString("Nagraj: R", 445, 30);
        g.drawString("Odtworz: P", 430, 50);
        g.setColor(Color.RED);
        if(record) g.fillOval(600, 60, 20, 20);
        
        //Debug screen
        /*g.setFont(new Font("Calibri",Font.BOLD,20));
        g.setColor(Color.RED);
        g.drawString("GRACZ Y: " + mainPlayer.getY(), 20, 30);
        g.drawString("YVELOCITY: " + ((int)mainPlayer.getYVelocity()), 20, 50);
        g.drawString("KAMERA: " + cameraY, 20, 70);*/
        
        /*g.drawString(walls.get(0).id + "SCIANA1 X: " + walls.get(0).x, 20, 100);
        //g.drawString(walls.get(5).id + "SCIANA2 X: " + walls.get(5).x, 20, 120);
        g.drawString(walls.get(4).id + "SCIANA3 X: " + walls.get(4).x, 20, 140);
        g.drawString(walls.get(3).id + "SCIANA4 X: " + walls.get(3).x, 20, 160);
        g.drawString(walls.get(2).id + "SCIANA5 X: " + walls.get(2).x, 20, 180);
        g.drawString(walls.get(1).id + "SCIANA6 X: " + walls.get(1).x, 20, 200);
        
        g.drawString("| SCIANA1 Y: " + walls.get(0).y, 160, 100);
        //g.drawString("| SCIANA2 Y: " + walls.get(5).y, 160, 120);
        g.drawString("| SCIANA3 Y: " + walls.get(4).y, 160, 140);
        g.drawString("| SCIANA4 Y: " + walls.get(3).y, 160, 160);
        g.drawString("| SCIANA5 Y: " + walls.get(2).y, 160, 180);
        g.drawString("| SCIANA6 Y: " + walls.get(1).y, 160, 200);*/

       /* g.drawString("Wysokosc: " + licznikWys, 500, 30);
        g.drawString("Prawdopodobienstwo: " + prawdRuchomego, 400, 50);
        g.drawString("SC1 Move: " + walls.get(0).ruchoma, 500, 70);
        g.drawString("SC2 Move: " + walls.get(5).ruchoma, 500, 90);
        g.drawString("SC3 Move: " + walls.get(4).ruchoma, 500, 110);
        g.drawString("SC4 Move: " + walls.get(3).ruchoma, 500, 130);
        g.drawString("SC5 Move: " + walls.get(2).ruchoma, 500, 150);
        g.drawString("SC6 Move: " + walls.get(1).ruchoma, 500, 170);
        g.drawString("XVELOCITY: " + ((int)mainPlayer.getXVelocity()), 500, 190);
        g.drawString("Intersect: " + mainPlayer.onAnyPlatform, 500, 210);
		*/
        
    }

    public void processInput(){
        mainPlayer.handleInput();
        if(record){
            try {
                RecordStream.writeInt(mainPlayer.spriteId);
                RecordStream.writeInt(mainPlayer.getX());
                RecordStream.writeInt(mainPlayer.getY());
                for (Wall wall: walls){
                    RecordStream.writeInt(wall.x);
                    RecordStream.writeInt(wall.y);
                }
                RecordStream.writeInt(licznikWys);
            }catch (IOException exception) {
                exception.printStackTrace();
            }
        }
    }

    public void update(){
        mainPlayer.update();
        prawdRuchomego = (licznikWys / 500d) >= 1 ? 1 : (licznikWys/500d); // Prawdopodobienstwo rosnie wraz z wysokoscia
        //Wprawienie w ruch platformy
        for(Wall wall: walls) {
            if (wall.ruchoma) {
                wall.ruch();
            }
        }
    }

    public void playRecord(Graphics g){
        try {

            tlo = new ImageIcon("img/tlorc.png").getImage();
            platforma = new ImageIcon("img/platformrc.png").getImage();
            g.drawImage(tlo, 0, 0, null);
            Image Sprite = mainPlayer.frontIm;
            switch(PlayStream.readInt()) {
                case 1:
                    Sprite = mainPlayer.frontIm;
                    break;
                case 2:
                    Sprite = mainPlayer.leftIm;
                    break;
                case 3:
                    Sprite = mainPlayer.rightIm;;
                    break;
                case 4:
                    Sprite = mainPlayer.jumpIm;
                    break;
                case 5:
                    Sprite = mainPlayer.jump_l_Img;
                    break;
                case 6:
                    Sprite = mainPlayer.jump_r_Img;
                    break;
            }

            g.drawImage(Sprite, PlayStream.readInt(), PlayStream.readInt(), null);
            g.setColor(new Color(132,109,76));
            for(int i = 0; i < walls.size(); i++) {
                g.drawImage(platforma,PlayStream.readInt(),PlayStream.readInt(),null);
            }
            g.setFont(new Font("Silkscreen Expanded",Font.TRUETYPE_FONT,30));
            g.setColor(Color.DARK_GRAY);
            g.drawString("Wysokosc:" + PlayStream.readInt(), 10, 30);
            g.setFont(new Font("Silkscreen Expanded",Font.TRUETYPE_FONT,25));
            g.drawString("Przerwij: P", 415, 30);
            g.drawString("Wyjscie: esc", 10, 450);

        }catch (Exception e){
            e.printStackTrace();
            play = false;
        }
    }

}
