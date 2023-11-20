package com.coco3x.travelpathfinder.util;

import org.springframework.stereotype.Component;

import java.io.*;
import java.util.List;

@Component
public class Crawler {
    private static final String cmd = "python3";
    private static final String fileName = "crawling_controller1.py";
    private static final String filePath = "/Users/coco3x/development/project/travel-pathfinder/crawler";
    private static final Object obj = new Object();
    private final Process process;
    private final BufferedReader br;
    private final BufferedWriter bw;

    private Crawler(){
        ProcessBuilder pb = new ProcessBuilder(cmd, fileName);
        pb.directory(new File(filePath));
        try {
            process = pb.start();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        br = new BufferedReader(new InputStreamReader(process.getInputStream()));
        bw = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));
    }

    public String command(String cmd){
        try {
            //명령어 입력
            bw.write(cmd);
            bw.newLine();
            bw.flush();

            //결과 리턴
            return br.readLine();

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
