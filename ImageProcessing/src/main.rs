extern crate image;

use image::{open, Pixel, Primitive, Rgb, RgbImage};
use std::time::Instant;
use std::convert::{From, Into, TryFrom};

fn modified_name(s: &str) -> String {
    let basename = s.split('.').next().unwrap();
    let mut result = basename.to_string();
    result.push_str("_b.jpg");
    result
}

struct Accumulator {
    value: Rgb<u32>,
}

impl Accumulator {
    fn add<T: Into<u32> + Primitive>(&mut self, pix: &Rgb<T>) {
        for channel in 0..3 {
            self.value[channel] += pix[channel].into();
        }
    }

    fn sub<T: Into<u32> + Primitive>(&mut self, pix: &Rgb<T>) {
        for channel in 0..3 {
            self.value[channel] -= pix[channel].into();
        }
    }

    fn mean<T: From<u8> + TryFrom<u32> + Primitive>(&self, width: u32) -> Rgb<T> {
        let mut mean: [T; 3] = [0.into(), 0.into(), 0.into()];
        for channel in 0..3 {
            let avg: u32 = self.value[channel] / width;
            let res_or_err: Result<T, _> = T::try_from(avg);
            let res_or_none: Option<T> = res_or_err.ok();
            let res: T = res_or_none.unwrap();
            mean[channel] = res;
        }
        Rgb::<T>(mean)
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

    let (cycles, length) = if horizontal {
        (img.height(), img.width())
    } else {
        (img.width(), img.height())
    };
    let get_px = if horizontal {
        retrieve_pixel
    } else {
        retrieve_pixel_swap
    };
    let put_px = if horizontal {
        place_pixel
    } else {
        place_pixel_swap
    };

    for i in 0..cycles {
        let mut trailing;
        let mut leading;
        let mut acc = Accumulator {
            value: Rgb([0, 0, 0]),
        };

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

fn unsharp_mask(clear: RgbImage, radius: u32) -> RgbImage {
    let mut clear = clear;
    let blurry = gaussian_blur(clear.clone(), radius);

    for (clear, blurry) in clear.pixels_mut().zip(blurry.pixels()) {
        for channel in 0..3 {
            let clear_val = clear[channel] as i32;
            let blurry_val = blurry[channel] as i32;
            clear[channel] = clear_val
                .saturating_add((clear_val - blurry_val) * 1)
                .clamp(0, 255) as u8;
        }
    }
    clear
}

fn gaussian_blur(img: RgbImage, radius: u32) -> RgbImage {
    let mut img = img;
    for _ in 0..3 {
        img = directional_blur(&img, true, radius);
        img = directional_blur(&img, false, radius);
    }
    img
}

fn guided_blur(img: RgbImage, radius: u32, eps:u32) -> RgbImage {
    let mut new = RgbImage::new(img.width(), img.height());

    let mean = gaussian_blur(img.clone(), radius);
    let mut corr = mean.clone();
    for pix in corr.iter_mut() {
        *pix = *pix * *pix;
    }
    corr = gaussian_blur(corr, radius);

    for (x,y,pix) in corr.enumerate_pixels_mut() {
        for channel in 0..3{
            pix[channel] = pix[channel] 
        }
    }

    new
}

fn main() {
    let name = "Pictures/Beach.jpg";
    let img = open(name).unwrap().to_rgb8();

    let time = Instant::now();
    let new = unsharp_mask(img, 100);

    println!("Milliseconds: {}", time.elapsed().as_millis());
    new.save("Pictures/tmp.jpg").unwrap();
}
