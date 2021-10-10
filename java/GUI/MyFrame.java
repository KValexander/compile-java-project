package com.main.GUI;

import javax.swing.JFrame;

public class MyFrame {

	JFrame frame = new JFrame();
	
	public MyFrame() {
		frame.setTitle("Main");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(500, 500);
		frame.setLayout(null);

		frame.setVisible(true);
	}
}