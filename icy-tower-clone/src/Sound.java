import java.io.File;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.FloatControl;

public class Sound {

    Clip clip;

    public void wybierzPlik(String soundFileName) {

        try {
            File plik = new File(soundFileName);
            AudioInputStream muzyczka = AudioSystem.getAudioInputStream(plik);
            clip = AudioSystem.getClip();
            clip.open(muzyczka);
        } catch (Exception e) {

        }
    }

    public void graj() {

        try {
            if (clip != null) clip.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void stop() {

        if (clip == null) return;
        clip.stop();

    }

    public void zapetl() {

        try {
            if (clip != null) {

                            clip.stop();
                            clip.setFramePosition(0);
                            clip.loop(Clip.LOOP_CONTINUOUSLY);

            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
    
    public void wyciszMuzyke() {
    	try {
            FloatControl poziomDzwieku = (FloatControl) clip.getControl(FloatControl.Type.MASTER_GAIN);
            poziomDzwieku.setValue(-70.0f);
    	}        
    	catch (Exception e) {
        e.printStackTrace();
    	}

    	
    }
    
    public void podglosnijMuzyke() {
        try {
            FloatControl poziomDzwieku = (FloatControl) clip.getControl(FloatControl.Type.MASTER_GAIN);
            poziomDzwieku.setValue(1.0f);
       	}        
       	catch (Exception e) {
        e.printStackTrace();
      	}
    }
    
}
