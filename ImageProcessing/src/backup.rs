extern crate image;

use image::{open, Pixel, Rgb, RgbImage};
use std::time::Instant;

fn modified_name(s: &str) -> String {
    let basename = s.split('.').next().unwrap();
    let mut result = basename.to_string();
    result.push_str("_b.jpg");
    result
}

struct Accumulator {
    value: [u32; 3],
}

impl Accumulator {
    fn add(&mut self, pix: &Rgb<u8>) {
        for channel in 0..3 {
            self.value[channel] += pix[channel] as u32;
        }
    }

    fn sub(&mut self, pix: &Rgb<u8>) {
        for channel in 0..3 {
            self.value[channel] -= pix[channel] as u32;
        }
    }

    fn mean(&self, width: u32) -> Rgb<u8> {
        let mut mean = [0, 0, 0];
        for channel in 0..3 {
            mean[channel] = (self.value[channel] / width) as u8;
        }
        *Pixel::from_slice(&mean)
    }
}

fn directional_blur(img: &RgbImage, horizontal: bool, radius: u32) -> RgbImage {
    let mut new = RgbImage::new(img.width(), img.height());

    fn retrieve_pixel(img: &RgbImage, a: u32, b: u32) -> &Rgb<u8> {
        img.get_pixel(a, b)
    }
    fn retrieve_pixel_swap(img: &RgbImage, a: u32, b: u32) -> &Rgb<u8> {
        img.get_pixel(b, a)
    }
    fn place_pixel(new: &mut RgbImage, a: u32, b: u32, p: Rgb<u8>) {
        new.put_pixel(a, b, p);
    }
    fn place_pixel_swap(new: &mut RgbImage, a: u32, b: u32, p: Rgb<u8>) {
        new.put_pixel(b, a, p);
    }

    let (cycles, length) = if horizontal { (img.height(), img.width()) }
                                    else { (img.width(), img.height()) };
    let get_px = if horizontal { retrieve_pixel } else { retrieve_pixel_swap };
    let put_px = if horizontal { place_pixel } else { place_pixel_swap };

    for i in 0..cycles {
        let mut trailing;
        let mut leading;
        let mut acc = Accumulator { value: [0, 0, 0] };

        //Pre filling accumulator
        for leading in 0..radius {
            acc.add(get_px(&img, leading, i));
        }
        //Doing starting image edge
        for center in 0..=radius {
            leading = center + radius;
            acc.add(get_px(&img, leading, i));
            put_px(&mut new, center, i, acc.mean(leading + 1));
        }
        // Doing whole image
        for center in radius + 1..length - radius {
            trailing = center - radius - 1;
            leading = center + radius;
            acc.add(get_px(&img, leading, i));
            acc.sub(get_px(&img, trailing, i));
            put_px(&mut new, center, i, acc.mean(leading - trailing));
        }
        //Doing rear edge
        for center in length - radius..length {
            trailing = center - radius;
            acc.sub(get_px(&img, trailing, i));
            put_px(&mut new, center, i, acc.mean(length - trailing));
        }
    }
    new
}

/*
fn unsharp_mask(img: &mut RgbImage) -> RgbImage{
    let blurry = gaussian_blur(*img,100);

    for (x,y,pix) in img.enumerate_pixels_mut(){
        let mut new_pix = [0,0,0];
        for channel in 0..3{
            pix[channel] = 
        }
        

    }
    *img
}*/

fn gaussian_blur(img: RgbImage, radius: u32) -> RgbImage {
    let mut img = img;
    for _ in 0..3 {
        img = directional_blur(&img, true, radius);
        img = directional_blur(&img, false, radius);
    }
    img
}

fn main() {
    let name = "Beach.jpg";
    let img = open(name).unwrap().to_rgb8();

    let time = Instant::now();
    let new = gaussian_blur(img,50);

    println!("Milliseconds: {}", time.elapsed().as_millis());
    new.save(modified_name(name)).unwrap();
}
