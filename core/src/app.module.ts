import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { GptModule } from './gpt/gpt.module';
import { UserModule } from './user/user.module';
import { PrismaModule } from './prisma/prisma.module';
import { PrismaService } from './prisma/prisma.service';
import { SuspicionModule } from './suspicion/suspicion.module';
import { FileModule } from './file/file.module';
  

@Module({
  imports: [GptModule, UserModule, SuspicionModule, PrismaModule, FileModule],
  controllers: [AppController],
  providers: [AppService,PrismaService],
})
export class AppModule {}
