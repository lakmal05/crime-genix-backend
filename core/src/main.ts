import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as express from 'express';
import { join } from 'path';
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use('/storage', express.static(join(__dirname, '..', 'storage')));
  await app.listen(5001);
}
bootstrap();
