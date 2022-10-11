package com.main.GUI;

import javax.swing.JFrame;

public class MyFrame extends JFrame{

	MyPanel panel;

	public MyFrame() {
		panel = new MyPanel();

		this.setTitle("JCA");
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		this.add(panel);
		
		this.pack();

		this.setLocationRelativeTo(null);
		this.setVisible(true);
	}
}