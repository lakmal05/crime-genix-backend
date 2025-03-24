import { Module } from '@nestjs/common';
import { SuspicionService } from './suspicion.service';
import { SuspicionController } from './suspicion.controller';
import { PrismaModule } from 'src/prisma/prisma.module';

@Module({
  imports:[PrismaModule],
  controllers: [SuspicionController],
  providers: [SuspicionService],
})
export class SuspicionModule {}
