import torch
import torch.nn as nn


class ConvBNReLU(nn.Module):
    def __init__(self, in_chs, out_chs, kernel_size, padding, leaky=False):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_chs,
                      out_chs,
                      kernel_size=kernel_size,
                      padding=padding), nn.BatchNorm2d(out_chs),
            nn.LeakyReLU(inplace=True) if leaky else nn.ReLU(inplace=True))

    def forward(self, x):
        return self.block(x)


class Encoder(nn.Module):
    def __init__(self, in_chs: int, mid_chs: int, out_chs: int,
                 kernel_size: int, padding: int):
        super().__init__()
        self.out_chs = out_chs
        self.block = nn.Sequential(
            ConvBNReLU(in_chs, mid_chs, kernel_size, padding),
            ConvBNReLU(mid_chs, out_chs, kernel_size, padding),
        )

    def forward(self, x):
        return self.block(x)


class Decoder(nn.Module):
    def __init__(self,
                 in_chs,
                 out_chs,
                 kernel_size,
                 padding,
                 scale_factor: int,
                 apply_dropout=False):
        super().__init__()
        self.out_chs = out_chs
        mid_chs = (in_chs + out_chs) // 2
        self.up = nn.Upsample(scale_factor=scale_factor,
                              mode='bilinear',
                              align_corners=True)
        self.block = nn.Sequential(
            ConvBNReLU(in_chs, mid_chs, kernel_size, padding),
            ConvBNReLU(mid_chs, out_chs, kernel_size, padding),
        )

        if apply_dropout:
            self.dropout = nn.Dropout(.25)
        else:
            self.dropout = None

    def forward(self, x1, x2):
        cat = torch.cat([self.up(x1), x2], dim=1)
        x = self.block(cat)
        if self.dropout:
            x = self.dropout(x)
        return x


class UNet(nn.Module):
    def __init__(self,
                 in_chs,
                 out_chs,
                 depth,
                 ini_chs=16,
                 kernel_size=3,
                 padding=1,
                 scale_factor=2):
        '''
        Args:
            depth (int): UNets depth i.e # of downsampling layers
            ini_chs (int): # of kernels in the first conv layer
        '''
        super().__init__()
        self.depth = depth
        self.encs = nn.ModuleList()
        self.decs = nn.ModuleList()
        self.pools = nn.ModuleList()
        chs = ini_chs
        for i in range(depth):
            enc = Encoder(in_chs if i == 0 else chs, chs, chs * 2, kernel_size,
                          padding)
            self.encs.append(enc)
            chs = chs * 2
            if i < (depth - 1):
                self.pools.append(nn.MaxPool2d(scale_factor))

        for i in range(depth - 1):
            enc_below = self.encs[-i - 1]
            enc_left = self.encs[-i - 2]
            dec = Decoder(enc_left.out_chs + enc_below.out_chs,
                          enc_left.out_chs,
                          kernel_size,
                          padding,
                          scale_factor,
                          apply_dropout=i < depth // 2)
            self.decs.append(dec)

        self.output_layer = nn.Conv2d(self.decs[-1].out_chs,
                                      out_chs,
                                      kernel_size=1,
                                      padding=0)

    def forward(self, x):
        skips = []
        for i in range(self.depth):
            x = self.encs[i](x)
            if i < (self.depth - 1):
                skips.append(x)
                x = self.pools[i](x)

        for i in range(self.depth - 1):
            x = self.decs[i](x, skips[-(i + 1)])

        return self.output_layer(x)


import sys
import argparse


def main():
    from torchsummary import summary
    parser = argparse.ArgumentParser(description='Print model summary.')
    parser.add_argument('--arch',
                        help='Save network architecture in svg',
                        metavar='<filename>')
    parser.add_argument('--shape',
                        help='Input shape. default: %(default)s',
                        metavar='<s1,s2,...>',
                        default='1,512,512')
    # parser.add_argument('-s','--switch', help='Switch argument',action='store_true')

    args = parser.parse_args()

    net = UNet(1, 1, 4)
    input_shape = [int(e) for e in args.shape.split(',')]
    summary(net, input_shape, depth=8, device='cpu')

    if args.arch:
        from pathlib import Path
        filename = Path(args.arch)
        import torchviz
        dummy_x = torch.zeros((1, *input_shape),
                              dtype=torch.float,
                              requires_grad=False)
        dummy_y = net(dummy_x)
        dot = torchviz.make_dot(dummy_y)
        dot.format = 'svg'
        dot.render(filename)


if __name__ == '__main__':
    sys.exit(main())