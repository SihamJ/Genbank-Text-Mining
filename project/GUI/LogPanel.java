package GUI;
import static GUI.Utils.*;

import java.awt.*;
import javax.swing.*;
import javax.swing.text.*;

public final class LogPanel extends Panel {
	
	private final static String title = "Log";
	private JTextPane textPane;
//	private ScrollPane scrollPanel;
	
	LogPanel() {
		super(title);
	}
	
	@Override
	protected void createComponents() {
		textPane = new JTextPane();
		SimpleAttributeSet attributeSet = new SimpleAttributeSet();  
	    StyleConstants.setBold(attributeSet, true);
	    textPane.setCharacterAttributes(attributeSet, true);  
	    textPane.setText("Log Log Log Loggggg");  
	    textPane.setForeground(white);
	   //scrollPanel = new ScrollPane();
	    
	}
	
	@Override
	protected void addComponents() {
		add(textPane, BorderLayout.CENTER);
//	add(scrollPanel, BorderLayout.EAST);
		
	}
	
	@Override
	protected void styleComponents() {
		textPane.setBackground(grey);
	}

}