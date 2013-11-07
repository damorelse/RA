import java.awt.BorderLayout;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import java.awt.GridBagLayout;
import javax.swing.JButton;
import java.awt.GridBagConstraints;
import java.awt.Insets;
import javax.swing.JTextArea;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JSplitPane;
import javax.swing.JTextPane;
import javax.swing.JLabel;
import java.awt.Canvas;
/*
import uk.co.caprica.vlcj.binding.LibVlc;
import uk.co.caprica.vlcj.runtime.RuntimeUtil;
import uk.co.caprica.vlcj.player.MediaPlayerFactory;
import uk.co.caprica.vlcj.player.embedded.EmbeddedMediaPlayer;
import uk.co.caprica.vlcj.player.embedded.videosurface.CanvasVideoSurface;
import uk.co.caprica.vlcj.runtime.windows.WindowsCanvas;
import com.sun.jna.Native;
import com.sun.jna.NativeLibrary;
*/

public class main_frame extends JFrame {

	/**
	 * Launch the application.
	 */
	
	
	
	public static void main(String[] args) {
		//System.loadLibrary("libvlc.so.5.3.2");
		//NativeLibrary.addSearchPath(
         //       "vlc", "/usr/lib"
         //   );
		//System.out.println(LibVlc.class);
		//Native.loadLibrary(RuntimeUtil.getLibVlcLibraryName(), LibVlc.class);
		//System.out.println("girija");
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					main_frame frame = new main_frame();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	/*public class mediaPlayer extends JFrame {
		public mediaPlayer() {
			setLayout(new BorderLayout());
			URL mediaURL = "";
			Player mediaPlayer = Manager.createRealizedPlayer(mediaURL);
			Component video = mediaPlayer.getVisualComponent();
            Component controls = mediaPlayer.getControlPanelComponent();
            add(video,BorderLayout.CENTER);
            add(controls,BorderLayout.SOUTH);
		}
	}*/
		

	/**
	 * Create the frame.
	 */
	public main_frame() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 450, 300);
		
		JMenuBar menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		
		JMenu mnFile = new JMenu("File");
		menuBar.add(mnFile);
		
		JMenuItem mntmNew = new JMenuItem("New");
		mnFile.add(mntmNew);
		
		JMenuItem mntmOpen = new JMenuItem("Open");
		mnFile.add(mntmOpen);
		
		JMenuItem mntmSave = new JMenuItem("Save");
		mnFile.add(mntmSave);
		
		JMenuItem mntmSaveAs = new JMenuItem("Save As");
		mnFile.add(mntmSaveAs);
		
		JMenuItem mntmQuit = new JMenuItem("Quit");
		mnFile.add(mntmQuit);
		
		JMenu mnEdit = new JMenu("Edit");
		menuBar.add(mnEdit);
		
		JMenuItem mntmCopy = new JMenuItem("Copy");
		mnEdit.add(mntmCopy);
		
		JMenuItem mntmPaste = new JMenuItem("Paste");
		mnEdit.add(mntmPaste);
		
		JMenuItem mntmSelect = new JMenuItem("Select All");
		mnEdit.add(mntmSelect);
		
		JMenuItem mntmUndo = new JMenuItem("Undo");
		mnEdit.add(mntmUndo);
		
		JMenuItem mntmRedo = new JMenuItem("Redo");
		mnEdit.add(mntmRedo);
		
		JMenu mnAnalysis = new JMenu("Analysis");
		menuBar.add(mnAnalysis);
		
		JMenu mnPlot = new JMenu("Plot");
		menuBar.add(mnPlot);
		
		JMenu mnHelp = new JMenu("Help");
		menuBar.add(mnHelp);
		GridBagLayout gridBagLayout = new GridBagLayout();
		gridBagLayout.columnWidths = new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
		gridBagLayout.rowHeights = new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
		gridBagLayout.columnWeights = new double[]{0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		gridBagLayout.rowWeights = new double[]{0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		getContentPane().setLayout(gridBagLayout);
		
		JButton btnHide = new JButton("Hide");
		GridBagConstraints gbc_btnHide = new GridBagConstraints();
		gbc_btnHide.insets = new Insets(0, 0, 5, 0);
		gbc_btnHide.gridx = 14;
		gbc_btnHide.gridy = 0;
		getContentPane().add(btnHide, gbc_btnHide);
		
		JPanel panel = new JPanel();
		GridBagConstraints gbc_panel = new GridBagConstraints();
		gbc_panel.gridheight = 8;
		gbc_panel.gridwidth = 10;
		gbc_panel.insets = new Insets(0, 0, 0, 5);
		gbc_panel.fill = GridBagConstraints.BOTH;
		gbc_panel.gridx = 2;
		gbc_panel.gridy = 1;
		getContentPane().add(panel, gbc_panel);
		GridBagLayout gbl_panel = new GridBagLayout();
		gbl_panel.columnWidths = new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
		gbl_panel.rowHeights = new int[]{0, 0, 0, 0, 0, 0, 0};
		gbl_panel.columnWeights = new double[]{1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, Double.MIN_VALUE};
		gbl_panel.rowWeights = new double[]{1.0, 0.0, 0.0, 0.0, 1.0, 1.0, Double.MIN_VALUE};
		panel.setLayout(gbl_panel);
		
		Canvas canvas = new Canvas();
		GridBagConstraints gbc_canvas = new GridBagConstraints();
		gbc_canvas.gridheight = 5;
		gbc_canvas.gridwidth = 9;
		gbc_canvas.insets = new Insets(0, 0, 5, 5);
		gbc_canvas.gridx = 0;
		gbc_canvas.gridy = 0;
		panel.add(canvas, gbc_canvas);
		System.out.println("girija2");
		//MediaPlayerFactory mediaPlayerFactory = new MediaPlayerFactory();
		System.out.println("girija3");
		//CanvasVideoSurface videoSurface = mediaPlayerFactory.newVideoSurface(canvas);
	    //EmbeddedMediaPlayer mediaPlayer = mediaPlayerFactory.newEmbeddedMediaPlayer();
	    //mediaPlayer.setVideoSurface(videoSurface);

	   // mediaPlayer.playMedia("/home/aparna/workspace/idn_coding/src/video1.mov");
		
		JTextPane txtpnMyNameIs = new JTextPane();
		txtpnMyNameIs.setText("My name is Aparna");
		GridBagConstraints gbc_txtpnMyNameIs = new GridBagConstraints();
		gbc_txtpnMyNameIs.gridwidth = 9;
		gbc_txtpnMyNameIs.fill = GridBagConstraints.BOTH;
		gbc_txtpnMyNameIs.gridx = 0;
		gbc_txtpnMyNameIs.gridy = 5;
		panel.add(txtpnMyNameIs, gbc_txtpnMyNameIs);
		
		
		
		JButton btnIdea = new JButton("Idea");
		GridBagConstraints gbc_btnIdea = new GridBagConstraints();
		gbc_btnIdea.insets = new Insets(0, 0, 5, 5);
		gbc_btnIdea.gridx = 12;
		gbc_btnIdea.gridy = 4;
		getContentPane().add(btnIdea, gbc_btnIdea);
		
		JButton btnTopic = new JButton("Topic");
		GridBagConstraints gbc_btnTopic = new GridBagConstraints();
		gbc_btnTopic.insets = new Insets(0, 0, 5, 5);
		gbc_btnTopic.gridx = 13;
		gbc_btnTopic.gridy = 4;
		getContentPane().add(btnTopic, gbc_btnTopic);
		
		JButton btnS_11 = new JButton("s10");
		GridBagConstraints gbc_btnS_11 = new GridBagConstraints();
		gbc_btnS_11.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_11.insets = new Insets(0, 0, 5, 5);
		gbc_btnS_11.gridx = 12;
		gbc_btnS_11.gridy = 5;
		getContentPane().add(btnS_11, gbc_btnS_11);
		
		JButton btnS_7 = new JButton("s11");
		GridBagConstraints gbc_btnS_7 = new GridBagConstraints();
		gbc_btnS_7.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_7.insets = new Insets(0, 0, 5, 5);
		gbc_btnS_7.gridx = 13;
		gbc_btnS_7.gridy = 5;
		getContentPane().add(btnS_7, gbc_btnS_7);
		
		JButton btnS_3 = new JButton("s12");
		GridBagConstraints gbc_btnS_3 = new GridBagConstraints();
		gbc_btnS_3.insets = new Insets(0, 0, 5, 0);
		gbc_btnS_3.gridx = 14;
		gbc_btnS_3.gridy = 5;
		getContentPane().add(btnS_3, gbc_btnS_3);
		
		JButton btnS_10 = new JButton("s7");
		GridBagConstraints gbc_btnS_10 = new GridBagConstraints();
		gbc_btnS_10.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_10.insets = new Insets(0, 0, 5, 5);
		gbc_btnS_10.gridx = 12;
		gbc_btnS_10.gridy = 6;
		getContentPane().add(btnS_10, gbc_btnS_10);
		
		JButton btnS_6 = new JButton("s8");
		GridBagConstraints gbc_btnS_6 = new GridBagConstraints();
		gbc_btnS_6.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_6.insets = new Insets(0, 0, 5, 5);
		gbc_btnS_6.gridx = 13;
		gbc_btnS_6.gridy = 6;
		getContentPane().add(btnS_6, gbc_btnS_6);
		
		JButton btnS_2 = new JButton("s9");
		GridBagConstraints gbc_btnS_2 = new GridBagConstraints();
		gbc_btnS_2.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_2.insets = new Insets(0, 0, 5, 0);
		gbc_btnS_2.gridx = 14;
		gbc_btnS_2.gridy = 6;
		getContentPane().add(btnS_2, gbc_btnS_2);
		
		JButton btnS_9 = new JButton("s4");
		GridBagConstraints gbc_btnS_9 = new GridBagConstraints();
		gbc_btnS_9.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_9.insets = new Insets(0, 0, 5, 5);
		gbc_btnS_9.gridx = 12;
		gbc_btnS_9.gridy = 7;
		getContentPane().add(btnS_9, gbc_btnS_9);
		
		JButton btnS_5 = new JButton("s5");
		GridBagConstraints gbc_btnS_5 = new GridBagConstraints();
		gbc_btnS_5.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_5.insets = new Insets(0, 0, 5, 5);
		gbc_btnS_5.gridx = 13;
		gbc_btnS_5.gridy = 7;
		getContentPane().add(btnS_5, gbc_btnS_5);
		
		JButton btnS_1 = new JButton("s6");
		GridBagConstraints gbc_btnS_1 = new GridBagConstraints();
		gbc_btnS_1.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_1.insets = new Insets(0, 0, 5, 0);
		gbc_btnS_1.gridx = 14;
		gbc_btnS_1.gridy = 7;
		getContentPane().add(btnS_1, gbc_btnS_1);
		
		JButton btnS_8 = new JButton("s1");
		GridBagConstraints gbc_btnS_8 = new GridBagConstraints();
		gbc_btnS_8.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_8.insets = new Insets(0, 0, 0, 5);
		gbc_btnS_8.gridx = 12;
		gbc_btnS_8.gridy = 8;
		getContentPane().add(btnS_8, gbc_btnS_8);
		
		JButton btnS_4 = new JButton("s2");
		GridBagConstraints gbc_btnS_4 = new GridBagConstraints();
		gbc_btnS_4.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS_4.insets = new Insets(0, 0, 0, 5);
		gbc_btnS_4.gridx = 13;
		gbc_btnS_4.gridy = 8;
		getContentPane().add(btnS_4, gbc_btnS_4);
		
		JButton btnS = new JButton("s3");
		GridBagConstraints gbc_btnS = new GridBagConstraints();
		gbc_btnS.fill = GridBagConstraints.HORIZONTAL;
		gbc_btnS.gridx = 14;
		gbc_btnS.gridy = 8;
		getContentPane().add(btnS, gbc_btnS);
		
		
	}

}
