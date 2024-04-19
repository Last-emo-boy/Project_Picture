import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';

function About() {
  return (
    <Container component="main" maxWidth="md">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ padding: 2, width: '100%', mt: 2 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            关于毕业照照片墙
          </Typography>
          <Typography variant="h6" component="h2" gutterBottom>
            项目背景
          </Typography>
          <Typography paragraph>
            “毕业照照片墙”是一个旨在为校友提供一个共享和回忆毕业照的平台。用户可以上传自己的毕业照，并浏览他人分享的照片，通过这个平台回顾校园生活，保持校友之间的联系。
          </Typography>
          <Typography variant="h6" component="h2" gutterBottom>
            主要功能
          </Typography>
          <Typography paragraph>
            - 上传功能：用户可以上传自己的毕业照，并添加简短的描述。
          </Typography>
          <Typography paragraph>
            - 浏览功能：用户可以浏览所有上传的毕业照，可以通过年份、专业等条件进行筛选。
          </Typography>
          <Typography paragraph>
            - 搜索功能：支持通过姓名或其他关键字搜索照片。
          </Typography>
          <Typography variant="h6" component="h2" gutterBottom>
            如何使用
          </Typography>
          <Typography paragraph>
            访问主页后，用户可以通过导航栏选择上传照片或浏览照片墙。在浏览页面，用户可以使用搜索栏进行搜索，或使用筛选器筛选特定的照片。
          </Typography>
          <Typography variant="h6" component="h2" gutterBottom>
            更多信息
          </Typography>
          <Typography paragraph>
            本项目由热心校友发起，旨在为毕业生提供一个永久的回忆录。我们希望每一位校友都能在这里找到属于自己的美好记忆。
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}

export default About;
