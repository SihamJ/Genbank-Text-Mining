package GUI;
import javax.swing.*;

import static GUI.Utils.*;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;

public class MainFrame extends JFrame {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private static String title = new String("Genbank");
	private final int width = 1230;
	private final int height = 800;
	
	private static MainFrame mainFrame;
	private JPanel mainContainer;
	private JPanel leftContainer;
	private JPanel rightContainer;
	private JPanel middleRightContainer;
	private TreePanel treePanel;
	private TitlePanel titlePanel;
	private MenuPanel menuPanel;
	private InfoPanel infoPanel;
	private LogPanel logPanel;
	private JPanel leftBottom;
	private ControlsPanel controlsPanel;
	private JPanel emptyPanel;
	private JMenu menuR;
	private JMenu menuK;
	private JMenuBar menuBar;
	
	private MainFrame() {
		super(title);
		initMainFrame();
		initComponents();
		initLayout();
		addComponents();
		style();
		setVisible(true);
	}
	
	public static MainFrame getSingleton() {
		if (mainFrame == null)
			mainFrame = new MainFrame();
		return mainFrame;
	}
	
	private void initLayout() {
		setLayout(new BorderLayout(40,55));
		mainContainer.setLayout(new FlowLayout(40, 40, 40));
		leftContainer.setLayout(new BorderLayout(10,40));
		rightContainer.setLayout(new BorderLayout(50,10));
		middleRightContainer.setLayout(new BorderLayout(50,10));
		leftBottom.setLayout(new GridLayout());
	}
	
	private void initMainFrame() {
		setSize(width, height);
		setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	private void initComponents() {
		mainContainer = new JPanel();
		logPanel = new LogPanel();
		infoPanel = new InfoPanel();
		menuPanel = new MenuPanel();
		titlePanel = new TitlePanel("GENBANK", 25, darkGrey);
		treePanel = new TreePanel();
		rightContainer = new JPanel();
		leftContainer = new JPanel();
		middleRightContainer = new JPanel();
		controlsPanel = new ControlsPanel();
		leftBottom = new JPanel();
		menuBar = new JMenuBar();
		menuK = new JMenu("choix des Kingdoms");
		menuR = new JMenu("Choix des Régions");
		menuK.setForeground(white);
		menuR.setForeground(white);
		for(int i=0; i < NB_ZONES; i++) {
			menuR.add(new JCheckBoxMenuItem("Region "+i));
		}
		for(int i=0; i < NB_ZONES; i++) {
			menuK.add(new JCheckBoxMenuItem("Kingdom "+i));
		}
	}
	private void addComponents() {
		menuBar.add(menuK);
		menuBar.add(menuR);
		menuBar.setBackground(grey);
		menuBar.setPreferredSize(new Dimension(1200, 40));
		setJMenuBar(menuBar);
		
		add(mainContainer, BorderLayout.CENTER);
		mainContainer.setPreferredSize(new Dimension(1300, 800));
		mainContainer.setBackground(black);
		mainContainer.add(leftContainer, FlowLayout.LEFT);
		leftContainer.setPreferredSize(new Dimension(400, 650));
		
		leftContainer.add(treePanel, BorderLayout.CENTER);
		//treePanel.setPreferredSize(new Dimension(400, 500));
		
		leftContainer.add(leftBottom, BorderLayout.SOUTH);
		leftContainer.setBackground(darkGrey);
		
		leftBottom.setBackground(grey);
		leftBottom.setPreferredSize(new Dimension(300,40));
		leftBottom.add(new EmptyPanel(grey));
		controlsPanel.setPreferredSize(new Dimension(300, 40));

		leftBottom.add(controlsPanel);
		leftBottom.add(new EmptyPanel(grey));
		
        mainContainer.add(rightContainer, FlowLayout.CENTER);
        rightContainer.setPreferredSize(new Dimension(700, 650));
		
       // rightContainer.add(titlePanel, BorderLayout.NORTH);
        titlePanel.setPreferredSize(new Dimension(700, 40));
        titlePanel.setBackground(black);
        rightContainer.setBackground(black);
        rightContainer.add(middleRightContainer, BorderLayout.CENTER);
        
        middleRightContainer.setPreferredSize(new Dimension(700,650));
        middleRightContainer.setBackground(black);
        
		middleRightContainer.add(infoPanel, BorderLayout.CENTER);
		infoPanel.setBackground(darkGrey);
		middleRightContainer.add(logPanel, BorderLayout.SOUTH);
		logPanel.setPreferredSize(new Dimension(700, 250));
		logPanel.setBackground(darkGrey);
	}
	
	private void style() {
		
	}
	
}