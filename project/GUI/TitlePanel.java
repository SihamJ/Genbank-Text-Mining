package GUI;
import static GUI.Utils.*;

import java.awt.*;
import javax.swing.*;

public class TitlePanel extends JPanel {
	
	private final JLabel title;
	private final int fontSize;
	private final Color backgroundColor;
	private final Color foregroundColor;
	
	public TitlePanel(String title, int fontSize, Color background) {
		this.title = new JLabel(title);
		this.fontSize = fontSize;
		this.backgroundColor = background;
		this.foregroundColor = white;
		
		initLayout();
		addComponents();
		swagComponent();
	}
	
	public TitlePanel(String title, int fontSize, Color background, Color foreground) {
		this.title = new JLabel(title);
		this.fontSize = fontSize;
		this.backgroundColor = background;
		this.foregroundColor = foreground;
		initLayout();
		addComponents();
		swagComponent();
	}
	
    private void initLayout() {
        this.setLayout(new BoxLayout(this, BoxLayout.X_AXIS));
        title.setLayout(new GridBagLayout());
    }

    private void addComponents() {
        this.add(Box.createHorizontalGlue());
        this.add(title, BorderLayout.CENTER);
        this.add(Box.createHorizontalGlue());
    }

    private void swagComponent() {
        this.setBackground(backgroundColor);
        this.setBorder(BorderFactory.createEmptyBorder(fontSize / 2, fontSize / 2, fontSize / 2, fontSize / 2));
        title.setForeground(foregroundColor);
        title.setFont(new Font(font, Font.PLAIN, fontSize));
    }
}