package com.main.GUI;

import java.awt.Font;

import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.ImageIcon;

public class MyPanel extends JPanel {

	ImageIcon image;
	JLabel label;

	MyPanel() {
		image = new ImageIcon("assets/corgi.png");
		
		label = new JLabel();
		label.setText("Java is compiled!");
		label.setIcon(image);
		label.setFont(new Font("Arial", Font.PLAIN, 50));

		this.add(label);
	}
}