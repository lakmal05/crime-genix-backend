import { Body, Controller, Get, Post } from '@nestjs/common';
import { GptService } from './gpt.service';

@Controller('gpt')
export class GptController {
  constructor(private readonly gptService: GptService) {}

  @Post('generate')
  generateFace(@Body() data: any) {
    return this.gptService.generateFace(data);
  }

  @Get('test')
  test(){
    return "true";
  }
}
